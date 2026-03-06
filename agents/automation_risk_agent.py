"""
Automation Risk Agent — Claude Version
────────────────────────────────────────────────────────────
Analyzes occupations and estimates their AI automation risk
using Claude.

Pipeline per occupation:
  1. Fetch profile from O*NET (tasks, skills, work context)
  2. Call Claude to score 6 dimensions (0-100 each)
  3. Output: score, level, horizon, recommendations

Run standalone:
    python run_automation.py

Requires in .env:
    ANTHROPIC_API_KEY=sk-ant-...
"""

import os
import json
import time
import requests
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv
import anthropic

load_dotenv()

ONET_BASE     = "https://services.onetcenter.org/ws"
ONET_USERNAME = os.getenv("ONET_USERNAME", "")
ONET_PASSWORD = os.getenv("ONET_PASSWORD", "")

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL  = "claude-sonnet-4-6"

# ── Risk level thresholds ─────────────────────────────────────────────────────

RISK_LEVELS = {
    "CRITICAL": {"min": 80, "color": "#DC2626", "emoji": "🔴"},
    "HIGH":     {"min": 60, "color": "#EA580C", "emoji": "🟠"},
    "MEDIUM":   {"min": 40, "color": "#CA8A04", "emoji": "🟡"},
    "LOW":      {"min": 20, "color": "#16A34A", "emoji": "🟢"},
    "SAFE":     {"min":  0, "color": "#2563EB", "emoji": "🔵"},
}

def classify_risk(score: float) -> str:
    if score >= 80: return "CRITICAL"
    if score >= 60: return "HIGH"
    if score >= 40: return "MEDIUM"
    if score >= 20: return "LOW"
    return "SAFE"


# ── Default occupations to analyze ───────────────────────────────────────────

DEFAULT_OCCUPATIONS = [
    {"code": "43-3031.00", "title": "Bookkeeping, Accounting & Auditing Clerks"},
    {"code": "43-4051.00", "title": "Customer Service Representatives"},
    {"code": "43-9022.00", "title": "Word Processors and Typists"},
    {"code": "51-2099.00", "title": "Assemblers and Fabricators"},
    {"code": "53-3032.00", "title": "Heavy and Tractor-Trailer Truck Drivers"},
    {"code": "41-2031.00", "title": "Retail Salespersons"},
    {"code": "13-2011.00", "title": "Accountants and Auditors"},
    {"code": "41-3031.00", "title": "Financial Services Sales Agents"},
    {"code": "15-1211.00", "title": "Computer Systems Analysts"},
    {"code": "27-3043.00", "title": "Writers and Authors"},
    {"code": "13-1111.00", "title": "Management Analysts"},
    {"code": "29-1141.00", "title": "Registered Nurses"},
    {"code": "25-2021.00", "title": "Elementary School Teachers"},
    {"code": "19-3011.00", "title": "Economists"},
    {"code": "23-1011.00", "title": "Lawyers"},
    {"code": "21-1021.00", "title": "Child, Family & School Social Workers"},
]


class AutomationRiskAgent:
    def __init__(self):
        self.onet_auth = (ONET_USERNAME, ONET_PASSWORD) if ONET_USERNAME else None
        self.onet_session = requests.Session()
        if self.onet_auth:
            self.onet_session.auth = self.onet_auth
            self.onet_session.headers.update({"Accept": "application/json"})

    # ── Claude call ───────────────────────────────────────────────────────────

    def _call_claude(self, system: str, user: str, max_tokens: int = 900) -> str:
        """Call Claude and return the text response, stripping any markdown fences."""
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            system=system,
            messages=[
                {"role": "user", "content": user},
            ],
        )
        text = response.content[0].text.strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.rsplit("```", 1)[0].strip()
        return text

    # ── O*NET profile ─────────────────────────────────────────────────────────

    def _get_occupation_profile(self, code: str, title: str) -> dict:
        """Fetch tasks, skills, work context from O*NET."""
        profile = {
            "code": code, "title": title,
            "tasks": [], "skills": [], "work_context": [],
        }
        if not self.onet_auth:
            return profile

        for key, url in {
            "tasks":        f"{ONET_BASE}/occupations/{code}/details/tasks",
            "skills":       f"{ONET_BASE}/occupations/{code}/details/skills",
            "work_context": f"{ONET_BASE}/occupations/{code}/details/work_context",
        }.items():
            try:
                r = self.onet_session.get(url, timeout=8)
                if r.status_code == 200:
                    items = r.json().get("element", r.json().get("category", []))
                    profile[key] = [i.get("name", i.get("title", "")) for i in items[:8]]
            except Exception:
                pass
        return profile

    # ── Claude risk assessment ────────────────────────────────────────────────

    def _assess_risk(self, profile: dict) -> dict:
        """Use Claude to score automation risk across 6 dimensions."""
        tasks_str   = "\n".join(f"  - {t}" for t in profile["tasks"])        or "  (not available)"
        skills_str  = "\n".join(f"  - {s}" for s in profile["skills"])       or "  (not available)"
        context_str = "\n".join(f"  - {c}" for c in profile["work_context"]) or "  (not available)"

        system = (
            "You are a senior labor economist specializing in AI and automation impact. "
            "Evaluate occupation automation risk across 6 dimensions using rigorous analysis. "
            "Consider LLMs, robotics, computer vision, and RPA. "
            "Respond ONLY with a valid JSON object — no extra text or markdown."
        )

        user = f"""Assess the AI automation risk for:

OCCUPATION: {profile["title"]}
SOC CODE:   {profile["code"]}

TASKS:
{tasks_str}

SKILLS REQUIRED:
{skills_str}

WORK CONTEXT:
{context_str}

Return exactly this JSON:
{{
  "automation_score": <integer 0-100>,
  "risk_level": "<CRITICAL|HIGH|MEDIUM|LOW|SAFE>",
  "time_horizon": "<1-3 years|3-7 years|7+ years|unlikely>",
  "dimensions": {{
    "routinization": <integer 0-100>,
    "ai_capability_current": <integer 0-100>,
    "human_interaction_required": <integer 0-100>,
    "creativity_required": <integer 0-100>,
    "physical_dexterity": <integer 0-100>,
    "ethical_judgment": <integer 0-100>
  }},
  "tasks_at_risk": ["<task1>", "<task2>", "<task3>"],
  "resilient_tasks": ["<task1>", "<task2>"],
  "threatening_technologies": ["<tech1>", "<tech2>", "<tech3>"],
  "reasoning": "<2-3 sentences explaining the score>",
  "worker_recommendation": "<concrete action for the worker>",
  "policy_recommendation": "<recommended public policy>"
}}"""

        try:
            text   = self._call_claude(system, user, max_tokens=1500)
            result = json.loads(text)
            result["automation_score"] = float(result.get("automation_score", 50))
            result["risk_level"]       = classify_risk(result["automation_score"])
            return result
        except Exception as e:
            print(f"    [!] Claude error for {profile['title']}: {e}")
            return self._fallback_assessment(profile)

    def _fallback_assessment(self, profile: dict) -> dict:
        """Heuristic fallback when OpenAI API is unavailable."""
        title = profile["title"].lower()
        score = 50.0
        if any(k in title for k in ["clerk", "typist", "assembler", "driver", "cashier"]):
            score = 72.0
        elif any(k in title for k in ["nurse", "teacher", "lawyer", "social worker", "economist"]):
            score = 22.0
        return {
            "automation_score":         score,
            "risk_level":               classify_risk(score),
            "time_horizon":             "3-7 years",
            "dimensions": {
                "routinization":              score,
                "ai_capability_current":      score * 0.8,
                "human_interaction_required": 100 - score,
                "creativity_required":        100 - score,
                "physical_dexterity":         30.0,
                "ethical_judgment":           100 - score,
            },
            "tasks_at_risk":            ["Routine information processing"],
            "resilient_tasks":          ["Complex human interaction", "Contextual judgment"],
            "threatening_technologies": ["LLMs", "RPA", "Computer Vision"],
            "reasoning":                "Heuristic estimate — Claude API unavailable.",
            "worker_recommendation":    "Develop management and human interaction skills.",
            "policy_recommendation":    "Reskilling programs and digital upskilling.",
        }

    # ── Policy report ─────────────────────────────────────────────────────────

    def _generate_policy_report(self, results: list[dict]) -> dict:
        """Generate public policy recommendations using Claude."""
        df        = pd.DataFrame(results)
        high_risk = df[df["automation_score"] >= 60]["title"].tolist()
        avg_score = df["automation_score"].mean()
        dist      = df["risk_level"].value_counts().to_dict()

        summary = {
            "total_occupations": len(results),
            "average_score":     round(avg_score, 1),
            "risk_distribution": dist,
            "high_exposure_jobs": high_risk[:5],
        }

        system = (
            "You are a labor policy advisor for governments. "
            "Write in formal English. "
            "Respond ONLY with a valid JSON object — no extra text."
        )

        user = f"""Based on this automation risk analysis of {len(results)} occupations:

{json.dumps(summary, indent=2)}

Return exactly this JSON:
{{
  "overall_diagnosis": "<2-3 sentences on the labor market outlook>",
  "policy_urgency": "<HIGH|MEDIUM|LOW>",
  "priority_policies": [
    {{"name": "<n>", "description": "<1 sentence>", "target_population": "<group>", "horizon": "<short/medium/long term>"}},
    {{"name": "<n>", "description": "<1 sentence>", "target_population": "<group>", "horizon": "<short/medium/long term>"}},
    {{"name": "<n>", "description": "<1 sentence>", "target_population": "<group>", "horizon": "<short/medium/long term>"}},
    {{"name": "<n>", "description": "<1 sentence>", "target_population": "<group>", "horizon": "<short/medium/long term>"}}
  ],
  "priority_sectors": ["<sector1>", "<sector2>", "<sector3>"],
  "monitoring_indicators": ["<indicator1>", "<indicator2>", "<indicator3>"],
  "key_message": "<one impactful sentence for public communication>"
}}"""

        try:
            text = self._call_claude(system, user, max_tokens=1200)
            return json.loads(text)
        except Exception as e:
            print(f"  [!] Policy report error: {e}")
            return {
                "overall_diagnosis":     f"{round(len(high_risk)/len(results)*100)}% of analyzed occupations face high automation exposure.",
                "policy_urgency":        "HIGH",
                "priority_policies": [
                    {"name": "National Digital Reskilling Program", "description": "Retrain high-risk workers toward AI-complementary skills.", "target_population": "Workers in high-risk occupations", "horizon": "short term"},
                    {"name": "Adaptive Labor Safety Net",           "description": "Extended unemployment linked to transition programs.",       "target_population": "Displaced workers",               "horizon": "short term"},
                    {"name": "AI Supervision Certifications",       "description": "National standards for workers supervising AI systems.",     "target_population": "Technical professionals",         "horizon": "medium term"},
                    {"name": "Automation Transition Tax",           "description": "Tax on mass AI-driven layoffs to fund retraining.",          "target_population": "Large employers",                 "horizon": "medium term"},
                ],
                "priority_sectors":      ["Administrative Services", "Transportation", "Retail"],
                "monitoring_indicators": ["AI-driven displacement rate", "Reskilling participation rate", "Wage polarization index"],
                "key_message":           "Without proactive policy, automation will deepen inequality — with it, AI can become the greatest driver of social mobility.",
            }

    # ── Main pipeline ─────────────────────────────────────────────────────────

    def run(self, occupations: list[dict] = None, delay: float = 0.3) -> dict:
        """
        Full automation risk analysis pipeline.

        Args:
            occupations: list of {"code": str, "title": str}
                         Defaults to DEFAULT_OCCUPATIONS (16 occupations).
            delay:       seconds between API calls to avoid rate limits.

        Returns:
            {
                "results":       list of per-occupation assessments,
                "policy_report": public policy recommendations,
                "metadata":      summary statistics,
            }
        """
        occupations = occupations or DEFAULT_OCCUPATIONS

        print(f"\n{'='*60}")
        print(f"  Automation Risk Agent — powered by {MODEL}")
        print(f"  {datetime.now().strftime('%d %b %Y %H:%M')}")
        print(f"  Analyzing {len(occupations)} occupations...")
        print(f"{'='*60}")

        results = []
        for i, occ in enumerate(occupations):
            print(f"\n  [{i+1}/{len(occupations)}] {occ['title']}")
            profile    = self._get_occupation_profile(occ["code"], occ["title"])
            assessment = self._assess_risk(profile)
            record     = {"code": occ["code"], "title": occ["title"], **assessment}
            results.append(record)
            cfg = RISK_LEVELS[record["risk_level"]]
            print(f"     {cfg['emoji']}  Score: {record['automation_score']:.0f}/100 — {record['risk_level']}")
            if i < len(occupations) - 1:
                time.sleep(delay)

        print("\n  Generating policy report...")
        policy_report = self._generate_policy_report(results)
        avg_score     = sum(r["automation_score"] for r in results) / len(results)

        print(f"\n{'='*60}")
        print(f"  ✓ Done. Average score: {avg_score:.1f}/100")
        print(f"{'='*60}\n")

        return {
            "results":       results,
            "policy_report": policy_report,
            "metadata": {
                "total_occupations": len(results),
                "analysis_date":     datetime.now().isoformat(),
                "average_score":     round(avg_score, 1),
                "model_used":        MODEL,
                "distribution": {
                    level: sum(1 for r in results if r["risk_level"] == level)
                    for level in RISK_LEVELS
                },
            },
        }