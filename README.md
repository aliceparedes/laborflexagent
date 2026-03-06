# LaborFlex

**AI-powered labor market intelligence platform**  
*Kautz-Uible Economics Institute · University of Cincinnati*

---

## Overview

LaborFlex is a multi-agent AI system that collects real-time labor market data, performs economic and automation risk analysis using Claude AI, and generates professional Excel dashboards and PDF briefings — all from a single Streamlit interface.

---

## Architecture

```
app.py (Streamlit Interface)
│
├── LaborDataAgent              agents/labor_data_agent.py
│   ├── Loads CSV files from data/
│   └── Fetches occupation profiles from O*NET Web Services API
│
├── EconomicAnalysisAgent       agents/economic_analysis_agent.py
│   ├── Unemployment trend analysis (Claude AI)
│   ├── Wage dynamics analysis (Claude AI)
│   ├── Structural/policy correlations (Claude AI)
│   └── Executive summary generation (Claude AI)
│
├── ReportAgent                 agents/report_agent.py
│   ├── Excel: 6-sheet labor market dashboard
│   └── PDF: Executive briefing with branded cover
│
├── AutomationRiskAgent         agents/automation_risk_agent.py
│   └── Scores occupations across 6 automation dimensions
│
└── AutomationReportAgent       agents/automation_report_agent.py
    ├── Excel: 4-sheet automation risk dashboard
    └── PDF: Policy briefing with occupation deep dives
```

---

## Features

**Tab 1 — Labor Market Analysis**
- Pulls BLS unemployment, wage, and job openings data from CSV
- Fetches occupation demand signals from O*NET Web Services
- Runs full economic analysis via Claude AI
- Exports 6-sheet Excel dashboard + PDF briefing

**Tab 2 — Automation Risk Analysis**
- Analyzes 16 default occupations or a custom list
- Scores each across 6 dimensions: routinization, AI capability, human interaction, creativity, physical dexterity, ethical judgment
- Produces ranked risk index: `CRITICAL` / `HIGH` / `MEDIUM` / `LOW` / `SAFE`
- Exports Excel dashboard + PDF policy report with worker and policy recommendations

---

## Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure environment variables

Create a `.env` file in the project root:

```env
# O*NET Web Services
ONET_USERNAME=your@email.com
ONET_PASSWORD=your-api-key

# Anthropic Claude
ANTHROPIC_API_KEY=sk-ant-...

# OpenAI (automation risk agent)
OPENAI_API_KEY=sk-...
```

> Get a free O*NET API account at [services.onetcenter.org/developer/signup](https://services.onetcenter.org/developer/signup) — approval is typically instant for research use.

### 3. Add CSV data files

Place the following in the `data/` folder. If none are found, the system uses built-in sample data automatically.

**`data/unemployment.csv`**
```csv
date,unemployment_rate,labor_force_participation
2024-01-01,3.7,62.5
2024-02-01,3.9,62.4
```
> Source: [BLS series LNS14000000 + LNS11300000](https://data.bls.gov)

**`data/wage_growth.csv`**
```csv
date,sector,avg_hourly_wage,yoy_wage_growth_pct
2024-01-01,Healthcare,29.5,4.8
2024-01-01,Technology,47.0,6.5
```
> Source: [BLS Current Employment Statistics](https://www.bls.gov/ces/)

**`data/job_openings.csv`**
```csv
date,total_openings_millions,hires_millions
2024-01-01,9.5,6.1
2024-02-01,9.3,6.0
```
> Source: [BLS JOLTS](https://www.bls.gov/jlt/)

### 4. Run

```bash
streamlit run app.py
```

---

## Custom Occupation Analysis

In Tab 2, switch to **Custom list** mode and enter occupations one per line:

```
15-1252.00 | Software Developers
29-1141.00 | Registered Nurses
43-4051.00 | Customer Service Representatives
53-3032.00 | Heavy and Tractor-Trailer Truck Drivers
25-2021.00 | Elementary School Teachers
```

SOC codes available at [onetonline.org](https://www.onetonline.org).

---

## Outputs

All reports saved to `output/`:

| File | Contents |
|------|----------|
| `labor_market_YYYYMM.xlsx` | Cover · Executive Summary · Unemployment · Wage Growth · Occupation Profiles · Risk Factors |
| `labor_market_YYYYMM.pdf` | Branded cover · KPI tables · AI insights · Structural analysis |
| `automation_risk_YYYYMMDD_HHMM.xlsx` | Risk Dashboard · Detailed Analysis · Public Policy · Resilient Skills |
| `automation_risk_YYYYMMDD_HHMM.pdf` | KPI strip · Ranking table · Top-6 occupation deep dives · Policy recommendations |

---

## Project Structure

```
LABORFLEX/
├── app.py                          Streamlit interface
├── main.py                         CLI orchestrator
├── run_automation.py               CLI automation runner
├── requirements.txt
├── .env                            API credentials (not committed)
│
├── agents/
│   ├── __init__.py
│   ├── labor_data_agent.py         BLS + O*NET data collection
│   ├── economic_analysis_agent.py  Claude economic analysis
│   ├── report_agent.py             Labor market Excel + PDF
│   ├── automation_risk_agent.py    Occupation risk scoring
│   └── automation_report_agent.py  Automation Excel + PDF
│
├── data/                           CSV input files (not committed)
│   ├── unemployment.csv
│   ├── wage_growth.csv
│   └── job_openings.csv
│
└── output/                         Generated reports (not committed)
```

---

## Data Sources

| Source | Type | What it provides |
|--------|------|-----------------|
| BLS Public Data API | REST | Unemployment, wages, job openings |
| O*NET Web Services | REST | Occupation profiles, skills, demand signals |
| CSV files in `data/` | Local | Historical BLS time-series data |

---

## Extending the System

- **Policy Monitoring Agent** — Scrape DOL/BLS news and feed announcements into the analysis prompt for real-time policy signal detection
- **Forecasting Layer** — Apply ARIMA or regression to CSV data before analysis to generate 3–6 month forecasts
- **Regional Analysis** — Pull BLS state-level series IDs for metro-area intelligence
- **Additional O*NET Queries** — Change `ONET_KEYWORDS` in `main.py` to target sector-specific occupations

---

## .gitignore

```gitignore
.env
data/
output/
.venv/
__pycache__/
*.pyc
```

---

*Kautz-Uible Economics Institute · University of Cincinnati · March 2026*
