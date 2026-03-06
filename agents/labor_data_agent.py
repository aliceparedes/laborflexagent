"""
Labor Data Agent
────────────────────────────────────────────────────────────
Collects labor market data from three sources:
  1. CSV files in /data  (OEWS downloads from bls.gov/oes/tables.htm)
  2. BLS Public Data API (live time series: unemployment, wages, JOLTS)
  3. O*NET Web Services  (occupation profiles)

Usage:
    agent = LaborDataAgent()
    data  = agent.collect_all_data()
"""

import os
import requests
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# ── Paths & config ────────────────────────────────────────────────────────────
DATA_DIR     = Path(__file__).parent.parent / "data"
BLS_API_URL  = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
ONET_BASE    = "https://services.onetcenter.org/ws"

BLS_API_KEY    = os.getenv("BLS_API_KEY", "")
ONET_USERNAME  = os.getenv("ONET_USERNAME", "")
ONET_PASSWORD  = os.getenv("ONET_PASSWORD", "")

# Key BLS series for labor market analysis
BLS_SERIES = {
    "unemployment_rate":        "LNS14000000",   # Monthly unemployment %
    "labor_force_participation": "LNS11300000",  # Participation rate
    "avg_hourly_earnings":      "CES0500000003", # Private sector avg hourly earnings
    "job_openings":             "JTS000000000000000JO",  # Total job openings (JOLTS)
    "hires":                    "JTS000000000000000HI",  # Total hires (JOLTS)
}


class LaborDataAgent:
    def __init__(self):
        self.onet_auth = (ONET_USERNAME, ONET_PASSWORD) if ONET_USERNAME else None
        self.session = requests.Session()
        if self.onet_auth:
            self.session.auth = self.onet_auth
            self.session.headers.update({"Accept": "application/json"})

    # ── 1. CSV Loading (OEWS files) ───────────────────────────────────────────

    def load_csv_files(self) -> dict[str, pd.DataFrame]:
        """
        Load all CSV files from the /data directory.
        Expected files from BLS OEWS:
          - national_oews.csv   (from oesm24nat.zip)
          - unemployment.csv
          - wage_growth.csv
          - job_openings.csv
        """
        datasets = {}
        csv_files = list(DATA_DIR.glob("*.csv"))

        if not csv_files:
            print("[LaborDataAgent] No CSV files in /data — using sample data.")
            return self._sample_data()

        for path in csv_files:
            try:
                df = pd.read_csv(path)
                datasets[path.stem] = df
                print(f"[LaborDataAgent] Loaded {path.name}: {df.shape[0]} rows")
            except Exception as e:
                print(f"[LaborDataAgent] Could not load {path.name}: {e}")

        return datasets

    def _sample_data(self) -> dict[str, pd.DataFrame]:
        """Realistic sample data when no CSV files are present."""
        periods = pd.date_range("2022-01", periods=24, freq="MS")

        unemployment = pd.DataFrame({
            "date": periods,
            "unemployment_rate": [
                4.0, 3.9, 3.8, 3.7, 3.6, 3.5, 3.7, 3.8,
                3.9, 4.0, 4.1, 3.9, 3.8, 3.7, 3.6, 3.8,
                4.0, 4.1, 3.9, 3.8, 3.7, 3.9, 4.0, 3.9
            ],
            "labor_force_participation": [
                62.3, 62.4, 62.5, 62.6, 62.4, 62.3, 62.5, 62.6,
                62.7, 62.5, 62.3, 62.4, 62.6, 62.7, 62.8, 62.6,
                62.4, 62.3, 62.5, 62.7, 62.8, 62.6, 62.4, 62.5
            ],
        })

        wage_growth = pd.DataFrame({
            "date": list(periods[:8]) * 3,
            "sector": ["Healthcare"] * 8 + ["Technology"] * 8 + ["Services"] * 8,
            "avg_hourly_wage": [
                28.5, 28.9, 29.2, 29.6, 30.0, 30.3, 30.7, 31.1,
                45.0, 45.8, 46.5, 47.2, 47.9, 48.6, 49.3, 50.0,
                18.2, 18.4, 18.6, 18.8, 19.0, 19.2, 19.4, 19.7,
            ],
            "yoy_wage_growth_pct": [
                4.2, 4.5, 4.7, 4.8, 5.1, 5.3, 5.4, 5.6,
                6.1, 6.3, 6.5, 6.7, 6.9, 7.0, 7.2, 7.4,
                3.1, 3.2, 3.3, 3.5, 3.6, 3.7, 3.8, 4.0,
            ],
        })

        job_openings = pd.DataFrame({
            "date": periods,
            "total_openings_millions": [
                10.2, 10.5, 10.8, 11.0, 10.7, 10.4, 10.1, 9.8,
                9.5, 9.3, 9.1, 9.4, 9.6, 9.8, 10.0, 9.7,
                9.4, 9.2, 9.5, 9.7, 9.9, 9.6, 9.3, 9.5,
            ],
            "hires_millions": [
                6.3, 6.4, 6.5, 6.6, 6.4, 6.3, 6.1, 6.0,
                5.9, 5.8, 5.7, 5.9, 6.0, 6.1, 6.2, 6.0,
                5.9, 5.8, 6.0, 6.1, 6.2, 6.0, 5.9, 6.0,
            ],
        })

        return {
            "unemployment": unemployment,
            "wage_growth": wage_growth,
            "job_openings": job_openings,
        }

    # ── 2. BLS Public Data API ────────────────────────────────────────────────

    def get_bls_series(
        self,
        series_ids: list[str] = None,
        start_year: str = "2020",
        end_year: str = "2026",
    ) -> dict[str, pd.DataFrame]:
        """
        Pull BLS time series via the Public Data API v2.
        Returns {series_id: DataFrame with columns [year, period, value]}.

        Register free key at: https://data.bls.gov/registrationEngine/
        """
        ids = series_ids or list(BLS_SERIES.values())

        payload = {
            "seriesid":        ids,
            "startyear":       start_year,
            "endyear":         end_year,
            "calculations":    True,
            "annualaverage":   True,
        }
        if BLS_API_KEY:
            payload["registrationkey"] = BLS_API_KEY

        try:
            r = requests.post(BLS_API_URL, json=payload, timeout=15)
            r.raise_for_status()
            results = {}
            for series in r.json().get("Results", {}).get("series", []):
                sid = series["seriesID"]
                df  = pd.DataFrame(series["data"])
                df["value"] = pd.to_numeric(df["value"], errors="coerce")
                results[sid] = df
                label = next(
                    (k for k, v in BLS_SERIES.items() if v == sid), sid
                )
                print(f"[LaborDataAgent] BLS API → {label}: {len(df)} observations")
            return results
        except Exception as e:
            print(f"[LaborDataAgent] BLS API error: {e}")
            return {}

    # ── 3. O*NET Occupation Profiles ──────────────────────────────────────────

    def get_onet_occupations(self, keyword: str = "economist") -> list[dict]:
        """Search O*NET for occupations matching a keyword."""
        if not self.onet_auth:
            return self._sample_onet()
        try:
            url = f"{ONET_BASE}/occupations"
            r = self.session.get(url, params={"keyword": keyword, "end": 10}, timeout=8)
            r.raise_for_status()
            occupations = r.json().get("occupation", [])
            print(f"[LaborDataAgent] O*NET '{keyword}': {len(occupations)} results")
            return occupations
        except Exception as e:
            print(f"[LaborDataAgent] O*NET error: {e}")
            return self._sample_onet()

    def _sample_onet(self) -> list[dict]:
        return [
            {"code": "15-2051.00", "title": "Data Scientists"},
            {"code": "19-3011.00", "title": "Economists"},
            {"code": "13-2051.00", "title": "Financial Analysts"},
            {"code": "11-9199.00", "title": "Policy Analysts"},
        ]

    # ── Main collection pipeline ──────────────────────────────────────────────

    def collect_all_data(self) -> dict:
        """
        Run the full collection pipeline.
        Returns all datasets ready for analysis agents.
        """
        print("\n=== Labor Data Agent: Collecting ===")

        # 1. CSV / OEWS files
        csv_datasets = self.load_csv_files()

        # 2. BLS live time series
        bls_data = self.get_bls_series()

        # 3. O*NET occupations
        onet_raw = []
        for kw in ["economist", "data scientist", "policy analyst"]:
            onet_raw.extend(self.get_onet_occupations(kw))
        onet_df = pd.DataFrame(onet_raw).drop_duplicates(
            subset=["code"] if onet_raw else None
        )

        print("[LaborDataAgent] Collection complete.\n")
        return {
            "csv_datasets":    csv_datasets,
            "bls_series":      bls_data,
            "onet_occupations": onet_df,
        }