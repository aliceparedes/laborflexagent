"""
run_automation.py
────────────────────────────────────────────────────────────
Entry point for the Automation Risk Agent.

Analyzes occupations and estimates their AI automation risk,
then generates Excel + PDF reports in /output.

Usage:
    python run_automation.py

Configuration via .env file or environment variables:
    ANTHROPIC_API_KEY  = sk-ant-...
    ONET_USERNAME      = your_onet_username   (optional)
    ONET_PASSWORD      = your_onet_password   (optional)

Customize occupations:
    Edit CUSTOM_OCCUPATIONS below, or set to None to use
    the 16 default occupations built into the agent.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

# ── Optional: customize which occupations to analyze ─────────────────────────
# Set to None to use the default 16 occupations.
# Find SOC codes at: https://www.onetcenter.org/taxonomy.html

CUSTOM_OCCUPATIONS = None

# Example:
# CUSTOM_OCCUPATIONS = [
#     {"code": "15-1252.00", "title": "Software Developers"},
#     {"code": "29-1141.00", "title": "Registered Nurses"},
#     {"code": "43-4051.00", "title": "Customer Service Representatives"},
#     {"code": "53-3032.00", "title": "Heavy Truck Drivers"},
#     {"code": "25-2021.00", "title": "Elementary School Teachers"},
# ]
# ─────────────────────────────────────────────────────────────────────────────


def main():
    from agents.automation_risk_agent import AutomationRiskAgent
    from agents.automation_report_agent import AutomationReportAgent

    # Step 1 — Analyze occupations
    risk_agent = AutomationRiskAgent()
    analysis   = risk_agent.run(occupations=CUSTOM_OCCUPATIONS)

    # Step 2 — Generate reports
    report_agent = AutomationReportAgent()
    outputs      = report_agent.generate(analysis)

    print("\n✅ Done! Reports saved to /output:")
    for fmt, path in outputs.items():
        print(f"   [{fmt.upper()}] {path.name}")

    return outputs


if __name__ == "__main__":
    main()