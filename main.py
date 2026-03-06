"""
main.py
────────────────────────────────────────────────────────────
Entry point for the full Labor Market Intelligence pipeline.

Runs all agents in sequence:
  1. LaborDataAgent      → collect CSV + BLS API + O*NET data
  2. EconomicAnalysisAgent → AI trend analysis
  3. ReportAgent         → Excel + PDF labor market report

For automation risk analysis only, use:
    python run_automation.py

Usage:
    python main.py

Configuration via .env file or environment variables:
    ANTHROPIC_API_KEY  = sk-ant-...
    BLS_API_KEY        = your_bls_key      (optional, 500 req/day with key)
    ONET_USERNAME      = your_username     (optional)
    ONET_PASSWORD      = your_password     (optional)
"""

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def main():
    from agents.labor_data_agent import LaborDataAgent
    from agents.economic_analysis_agent import EconomicAnalysisAgent
    from agents.report_agent import ReportAgent

    print("=" * 60)
    print("  LABORFLEX — Labor Market Intelligence Agent")
    print("=" * 60)

    # ── Step 1: Collect data ─────────────────────────────────────────────────
    print("\n[1/3] Collecting labor market data...")
    t0   = time.time()
    data = LaborDataAgent().collect_all_data()
    print(f"  ✓ Data collected ({time.time()-t0:.1f}s)")

    # ── Step 2: AI analysis ──────────────────────────────────────────────────
    print("\n[2/3] Running AI economic analysis...")
    t0       = time.time()
    insights = EconomicAnalysisAgent().run_full_analysis(data)
    print(f"  ✓ Analysis complete ({time.time()-t0:.1f}s)")

    # Quick preview
    u = insights.get("unemployment", {})
    w = insights.get("wages", {})
    print(f"\n  Unemployment:  {u.get('trend_direction','N/A')} — {u.get('headline','')}")
    print(f"  Wage Trend:    {w.get('overall_wage_trend','N/A')}")
    print(f"  Sector Leaders:{', '.join(w.get('sector_leaders',[]))}")

    # ── Step 3: Generate reports ─────────────────────────────────────────────
    print("\n[3/3] Generating Excel + PDF reports...")
    t0      = time.time()
    outputs = ReportAgent().generate_reports(
        insights     = insights,
        csv_datasets = data.get("csv_datasets", {}),
    )
    print(f"  ✓ Reports generated ({time.time()-t0:.1f}s)")

    print("\n" + "=" * 60)
    print("  ✅ COMPLETE — Output files:")
    for fmt, path in outputs.items():
        print(f"     [{fmt.upper()}] {path.name}")
    print("=" * 60)

    return outputs


if __name__ == "__main__":
    main()