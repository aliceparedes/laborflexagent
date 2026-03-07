# Autonomous Labor Market Intelligence Agent - LaborFlex

## Executive Summary

The Autonomous Labor Market Intelligence Agent is a multi-agent AI system designed to analyze labor market conditions across sectors and occupations using unemployment, wage, job openings, and occupational skill data.

The system autonomously ingests labor market datasets, enriches them with occupational intelligence from the O*NET Web Services API, interprets labor market signals using Claude AI, and generates structured outputs in the form of Excel dashboards and PDF executive briefings.

Rather than simply summarizing data, the agent identifies structural patterns and relationships across labor indicators to help interpret how labor markets are evolving over time. The goal is to transform fragmented labor statistics into clear economic insights that can support workforce analysis, policy interpretation, and labor market research.

## Economic Problem and Relevance

Labor markets are dynamic systems that evolve across sectors, occupations, and time. Standard labor indicators such as unemployment rates or wage growth provide important information, but they often fail to explain the structural forces driving labor market changes.

Economists frequently analyze labor markets by examining multiple signals simultaneously. Unemployment rates capture labor market slack, wage growth may signal labor demand pressure or worker bargaining power, job openings reflect employer demand for labor, and occupational skill profiles help identify structural shifts in workforce requirements.

However, these indicators are typically analyzed separately. This project addresses the economic problem of integrating multiple labor market signals into a unified analysis framework capable of identifying structural labor market patterns.

By combining unemployment, wage, job openings, and occupation-level skill data, the system helps detect whether labor market changes reflect cyclical fluctuations, sector-specific demand changes, or broader structural shifts in labor demand.

Such insights are valuable for labor economists, workforce planners, policymakers, and organizations seeking to understand emerging labor market trends.

## Research Question

> **How can an autonomous AI agent detect and interpret structural changes in labor market conditions across sectors and occupations using unemployment, wage, job openings, and occupational skill data?**

## End Users

The outputs of this system are designed for users who need structured labor market intelligence rather than raw statistics. Potential users include:

- Labor economists and economic researchers
- Workforce development analysts
- Policymakers and public institutions
- Academic researchers studying labor markets
- Firms or organizations evaluating hiring conditions and labor risks

The system transforms raw labor statistics into interpretable outputs that support economic analysis and decision-making.

## Why This System Is Agentic

This project implements an agentic AI architecture in which multiple specialized agents perform distinct tasks within an autonomous workflow.

Unlike a simple chatbot or reporting script, the system operates as a coordinated analytical pipeline in which agents interact to perform sequential tasks.

The system autonomously:

1. Ingests labor market datasets from local sources.
2. Enriches those datasets with occupational intelligence from the O*NET Web Services API.
3. Assigns analytical tasks to specialized agents.
4. Interprets multiple labor indicators using economic reasoning.
5. Synthesizes findings into coherent labor market insights.
6. Generates professional reports without manual intervention.

This multi-step reasoning workflow demonstrates how agentic AI can automate complex economic analysis processes rather than simply generating text responses.

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

## Agent Roles
### LaborDataAgent

The LaborDataAgent performs data ingestion and enrichment tasks.

Its responsibilities include:

- Loading labor market CSV datasets
- Detecting and organizing economic indicators
- Retrieving occupational profiles from the O*NET Web Services API
- Preparing structured datasets for economic analysis

This agent ensures the system integrates both quantitative labor market indicators and occupation-level intelligence.

### Economic Analysis Agent
The EconomicAnalysisAgent performs economic interpretation and analysis.

Using Claude AI, the agent:

- Analyzes unemployment trends
- Interprets wage dynamics across sectors
- Examines job openings and hiring patterns
- Detects potential structural labor market signals
- Identifies possible economic risks
- Generates an executive summary of key findings

This agent transforms raw labor data into meaningful economic insights.

### Report Agent
The ReportAgent generates structured output artifacts for the user.

Its responsibilities include:

- Creating a five-sheet Excel dashboard
- Organizing economic insights alongside raw data
- Generating a professional PDF executive briefing
- Converting analysis results into user-ready reports

The outputs are designed to support economic interpretation and decision-making.

## System Workflow

The system follows a multi-stage analytical workflow:

###1. Data Ingestion
The LaborDataAgent loads unemployment, wage, and job openings datasets from the data/ directory.

###2. Data Enrichment
The agent retrieves occupational information from the O*NET API to add skill and occupation context.

###3. Indicator Analysis
The EconomicAnalysisAgent evaluates each labor indicator individually, identifying trends and anomalies.

###4. Cross-Indicator Interpretation
The system synthesizes signals across unemployment, wages, and job openings to detect broader labor market patterns.

###5. Executive Insight Generation
Claude AI generates a structured interpretation of the labor market conditions.

###6. Report Generation
The ReportAgent produces both Excel dashboards and a PDF briefing summarizing the analysis.






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
