# Autonomous Labor Market Intelligence Agent

## Overview

An AI-powered multi-agent system that collects labor market data, performs economic analysis using Claude AI, and generates professional Excel dashboards and PDF briefings.

## Research Question

> **How do labor market conditions evolve across occupations and sectors, and what structural trends are detectable from employment and wage data?**

## Agent Architecture

```
main.py (Orchestrator)
│
├── LaborDataAgent         (agents/labor_data_agent.py)
│   ├── Loads CSV files from data/
│   └── Fetches occupation data from O*NET Web Services API
│
├── EconomicAnalysisAgent  (agents/economic_analysis_agent.py)
│   ├── Analyzes unemployment trends (Claude AI)
│   ├── Analyzes wage dynamics (Claude AI)
│   ├── Estimates structural/policy correlations (Claude AI)
│   └── Generates executive summary (Claude AI)
│
└── ReportAgent            (agents/report_agent.py)
    ├── Excel: 5-sheet dashboard (openpyxl)
    └── PDF: Professional briefing (reportlab)
```

## Data Sources

| Source | Type | What it provides |
|--------|------|-----------------|
| CSV files in `data/` | Local | Unemployment, wage, job opening data |
| O*NET Web Services API | REST API | Occupation profiles, skills, demand signals |

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure O*NET credentials

Set environment variables:
```bash
export ONET_USERNAME="your_username"
export ONET_PASSWORD="your_password"
```

Or edit `main.py`:
```python
ONET_USERNAME = "your_username"
ONET_PASSWORD = "your_password"
```

Get a free O*NET API account at: https://services.onetcenter.org/

### 3. Add your CSV data files to `data/`

Supported file names (columns are auto-detected):
```
data/unemployment.csv   → expects: date, unemployment_rate, labor_force_participation
data/wage_growth.csv    → expects: date, sector, avg_hourly_wage, yoy_wage_growth_pct
data/job_openings.csv   → expects: date, total_openings_millions, hires_millions
```

If no CSVs are found, sample data is used automatically.

### 4. Run
```bash
python main.py
```

## Outputs

All outputs saved to `outputs/`:

| File | Description |
|------|-------------|
| `labor_market_report_YYYYMM.xlsx` | 5-sheet Excel dashboard |
| `labor_market_briefing_YYYYMM.pdf` | PDF executive briefing |

### Excel Sheets
1. **Executive Summary** — AI-generated KPIs and headline findings
2. **Unemployment Data** — Raw data + AI trend insight + chart
3. **Wage Growth** — Sector wage data + AI wage insight
4. **Occupation Profiles** — O*NET occupation data + structural analysis
5. **Risk Factors** — AI-identified labor market risks

## CSV Format Examples

### unemployment.csv
```csv
date,unemployment_rate,labor_force_participation
2024-01-01,3.7,62.5
2024-02-01,3.9,62.4
```

### wage_growth.csv
```csv
date,sector,avg_hourly_wage,yoy_wage_growth_pct
2024-01-01,Healthcare,29.5,4.8
2024-01-01,Technology,47.0,6.5
```

### job_openings.csv
```csv
date,total_openings_millions,hires_millions
2024-01-01,9.5,6.1
2024-02-01,9.3,6.0
```

## Extending the System

- **Add a Policy Monitoring Agent**: Scrape DOL/BLS news pages and feed announcements into the analysis prompt
- **Add Forecasting**: Use ARIMA or simple regression on the CSV data before passing to the analysis agent
- **Add More O*NET Queries**: Change `ONET_KEYWORDS` in `main.py` to search for occupations relevant to your sector
