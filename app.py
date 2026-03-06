"""
app.py — LaborFlex Streamlit Interface
Run with: streamlit run app.py
"""

import io
import sys
from pathlib import Path
from contextlib import redirect_stdout

import pandas as pd
import streamlit as st

sys.path.insert(0, str(Path(__file__).parent))

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="LaborFlex — Kautz-Uible Economics Institute",
    page_icon="📈",
    layout="wide",
)

# ── Design system ─────────────────────────────────────────────────────────────
# Aesthetic: Editorial / Data Journalism — The Economist meets FT
# UC Red #E00122 · Near-black #0D0D0D · Warm white #FAF9F7
# Accent ink #1C2B3A · Muted #8A9BAA · Rule color #DDD8D0

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800;900&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,300&family=DM+Mono:wght@400;500&display=swap');

/* ══════════════════════════════════════════════
   RESET & BASE
══════════════════════════════════════════════ */
*, *::before, *::after { box-sizing: border-box; }

:root {
    --red:       #E00122;
    --red-dark:  #A8011A;
    --ink:       #0D0D0D;
    --ink-soft:  #1C2B3A;
    --muted:     #6B7A8A;
    --rule:      #DDD8D0;
    --bg:        #FAF9F7;
    --surface:   #FFFFFF;
    --surface-2: #F4F2EE;
    --font-serif: 'Playfair Display', Georgia, serif;
    --font-sans:  'DM Sans', system-ui, sans-serif;
    --font-mono:  'DM Mono', 'Courier New', monospace;
}

.stApp, .main, section[data-testid="stMain"] {
    background-color: var(--bg) !important;
    font-family: var(--font-sans) !important;
}
.block-container {
    padding: 0 2rem 4rem !important;
    max-width: 1280px !important;
}
#MainMenu, footer, header { visibility: hidden; }

/* ══════════════════════════════════════════════
   MASTHEAD — newspaper front page energy
══════════════════════════════════════════════ */
.lf-flag {
    background: var(--ink);
    padding: 0;
    margin: 0 0 0 0;
    border-bottom: 3px solid var(--red);
}
.lf-flag-inner {
    display: flex;
    align-items: stretch;
    min-height: 96px;
}
.lf-flag-accent {
    width: 5px;
    background: var(--red);
    flex-shrink: 0;
}
.lf-flag-content {
    padding: 18px 32px 18px 28px;
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 24px;
}
.lf-flag-left {}
.lf-flag-kicker {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #FFFFFF;
    margin: 0 0 5px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.lf-flag-kicker::before {
    content: '';
    display: inline-block;
    width: 18px;
    height: 1.5px;
    background: var(--red);
    flex-shrink: 0;
}
.lf-flag-title {
    font-family: var(--font-serif);
    font-size: 1.85rem;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: -0.02em;
    margin: 0 0 4px;
    line-height: 1.1;
}
.lf-flag-sub {
    font-size: 0.74rem;
    color: #FFFFFF;
    letter-spacing: 0.04em;
    margin: 0;
    font-weight: 300;
}
.lf-flag-right {
    text-align: right;
    flex-shrink: 0;
}
.lf-flag-date {
    font-family: var(--font-mono);
    font-size: 0.66rem;
    color: #8A9BAA;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 6px;
}
.lf-flag-badge {
    display: inline-block;
    background: var(--red);
    color: white;
    font-family: var(--font-mono);
    font-size: 0.58rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 2px;
}

/* ══════════════════════════════════════════════
   SECTION LABELS — editorial ruling lines
══════════════════════════════════════════════ */
.lf-rule {
    display: flex;
    align-items: center;
    gap: 12px;
    margin: 32px 0 18px;
}
.lf-rule-text {
    font-family: var(--font-mono);
    font-size: 0.64rem;
    font-weight: 500;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--red);
    white-space: nowrap;
    flex-shrink: 0;
}
.lf-rule-line {
    height: 1px;
    background: var(--rule);
    flex: 1;
}

/* ══════════════════════════════════════════════
   KPI CARDS
══════════════════════════════════════════════ */
.lf-kpi-row {
    display: grid;
    gap: 12px;
    margin: 16px 0 24px;
}
.lf-kpi-row-4 { grid-template-columns: repeat(4, 1fr); }
.lf-kpi-row-5 { grid-template-columns: repeat(5, 1fr); }

.lf-kpi {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-top: 3px solid var(--ink-soft);
    padding: 16px 18px 14px;
    position: relative;
}
.lf-kpi::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 0;
    background: var(--red);
    transition: height 0.2s ease;
}
.lf-kpi:hover::after { height: 2px; }
.lf-kpi-label {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 0 0 8px;
}
.lf-kpi-value {
    font-family: var(--font-serif);
    font-size: 1.45rem;
    font-weight: 700;
    color: var(--ink);
    line-height: 1.1;
    margin: 0;
}
.lf-kpi-sub {
    font-size: 0.7rem;
    color: var(--muted);
    margin: 4px 0 0;
    font-weight: 300;
}

/* Risk color variants */
.lf-kpi.r-critical { border-top-color: #DC2626; }
.lf-kpi.r-critical .lf-kpi-value { color: #DC2626; }
.lf-kpi.r-high { border-top-color: #EA580C; }
.lf-kpi.r-high .lf-kpi-value { color: #EA580C; }
.lf-kpi.r-medium { border-top-color: #CA8A04; }
.lf-kpi.r-medium .lf-kpi-value { color: #CA8A04; }
.lf-kpi.r-low { border-top-color: #16A34A; }
.lf-kpi.r-low .lf-kpi-value { color: #16A34A; }

/* ══════════════════════════════════════════════
   PANELS
══════════════════════════════════════════════ */
.lf-card {
    background: var(--surface);
    border: 1px solid var(--rule);
    padding: 22px 26px;
    margin-bottom: 16px;
}
.lf-card-head {
    font-family: var(--font-mono);
    font-size: 0.62rem;
    font-weight: 500;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--muted);
    padding-bottom: 12px;
    border-bottom: 1px solid var(--rule);
    margin: 0 0 16px;
}
.lf-card p  { font-size: 0.9rem; color: var(--ink); line-height: 1.75; margin: 0 0 8px; font-weight: 300; }
.lf-card li { font-size: 0.9rem; color: var(--ink); line-height: 1.75; font-weight: 300; }
.lf-card strong { font-weight: 600; color: var(--ink-soft); }
.lf-card ul { padding-left: 16px; margin: 4px 0; }

/* ══════════════════════════════════════════════
   SUMMARY BLOCK — pull-quote style
══════════════════════════════════════════════ */
.lf-summary {
    background: var(--surface);
    border-left: 4px solid var(--red);
    border-top: 1px solid var(--rule);
    border-right: 1px solid var(--rule);
    border-bottom: 1px solid var(--rule);
    padding: 24px 28px;
    margin: 0 0 20px;
    font-size: 0.95rem;
    line-height: 1.85;
    color: var(--ink);
    font-weight: 300;
}
.lf-summary p { margin: 0 0 12px; }
.lf-summary p:last-child { margin: 0; }

/* ══════════════════════════════════════════════
   OCCUPATION RISK ROW
══════════════════════════════════════════════ */
.lf-occ-card {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-left: 4px solid var(--rule);
    padding: 16px 20px;
    margin-bottom: 10px;
    transition: border-color 0.15s, box-shadow 0.15s;
}
.lf-occ-card:hover {
    border-left-color: var(--red);
    box-shadow: 2px 0 12px rgba(224,1,34,0.06);
}
.lf-occ-header {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 10px;
    gap: 12px;
}
.lf-occ-title {
    font-family: var(--font-sans);
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--ink);
}
.lf-occ-score {
    font-family: var(--font-mono);
    font-size: 1.1rem;
    font-weight: 500;
    flex-shrink: 0;
}
.lf-score-bar-bg {
    height: 4px;
    background: var(--surface-2);
    border-radius: 0;
    margin-bottom: 10px;
    overflow: hidden;
}
.lf-score-bar {
    height: 100%;
    border-radius: 0;
    transition: width 0.8s cubic-bezier(0.4,0,0.2,1);
}
.lf-occ-meta {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    align-items: center;
}
.lf-tag {
    font-family: var(--font-mono);
    font-size: 0.6rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 2px 8px;
    border: 1px solid;
    border-radius: 2px;
}
.lf-tag-detail {
    font-size: 0.78rem;
    font-weight: 300;
    color: var(--muted);
    font-family: var(--font-sans);
    letter-spacing: 0;
    text-transform: none;
    border: none;
    padding: 0;
}

/* Risk tag colors */
.lf-tag-CRITICAL { color: #DC2626; border-color: #FCA5A5; background: #FEF2F2; }
.lf-tag-HIGH     { color: #EA580C; border-color: #FDBA74; background: #FFF7ED; }
.lf-tag-MEDIUM   { color: #CA8A04; border-color: #FDE68A; background: #FEFCE8; }
.lf-tag-LOW      { color: #16A34A; border-color: #86EFAC; background: #F0FDF4; }
.lf-tag-SAFE     { color: #2563EB; border-color: #BFDBFE; background: #EFF6FF; }

/* ══════════════════════════════════════════════
   POLICY CARDS
══════════════════════════════════════════════ */
.lf-policy-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin-bottom: 16px;
}
.lf-policy-card {
    background: var(--surface);
    border: 1px solid var(--rule);
    border-top: 3px solid var(--ink-soft);
    padding: 18px 20px;
}
.lf-policy-num {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--red);
    letter-spacing: 0.1em;
    margin-bottom: 6px;
}
.lf-policy-name {
    font-family: var(--font-serif);
    font-size: 1rem;
    font-weight: 700;
    color: var(--ink);
    margin: 0 0 8px;
    line-height: 1.3;
}
.lf-policy-desc {
    font-size: 0.84rem;
    color: var(--ink-soft);
    line-height: 1.65;
    margin: 0 0 10px;
    font-weight: 300;
}
.lf-policy-chips {
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
}
.lf-chip {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    padding: 2px 8px;
    background: var(--surface-2);
    color: var(--muted);
    border-radius: 2px;
    border: 1px solid var(--rule);
}

/* ══════════════════════════════════════════════
   KEY MESSAGE
══════════════════════════════════════════════ */
.lf-dispatch {
    background: var(--ink);
    border-left: 4px solid var(--red);
    padding: 18px 22px;
    margin-top: 14px;
}
.lf-dispatch-label {
    font-family: var(--font-mono);
    font-size: 0.58rem;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--red);
    margin-bottom: 6px;
}
.lf-dispatch-text {
    font-size: 0.92rem;
    font-weight: 400;
    line-height: 1.65;
    color: #CBD5E1;
}

/* ══════════════════════════════════════════════
   ABOUT STRIP
══════════════════════════════════════════════ */
.lf-about {
    background: var(--surface-2);
    border: 1px solid var(--rule);
    border-left: 3px solid var(--red);
    padding: 14px 20px;
    margin-bottom: 24px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
}
.lf-about-icon { font-size: 1.1rem; margin-top: 1px; flex-shrink: 0; }
.lf-about-text { font-size: 0.84rem; color: var(--ink-soft); line-height: 1.65; font-weight: 300; }
.lf-about-text strong { font-weight: 600; color: var(--ink); }

/* ══════════════════════════════════════════════
   STREAMLIT OVERRIDES
══════════════════════════════════════════════ */

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    border-bottom: 2px solid var(--rule) !important;
    background: transparent !important;
    padding: 0;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    padding: 12px 28px;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: var(--muted) !important;
    margin-bottom: -2px;
}
.stTabs [aria-selected="true"] {
    color: var(--red) !important;
    border-bottom: 2px solid var(--red) !important;
}
.stTabs [data-baseweb="tab"] span,
.stTabs [data-baseweb="tab"] p { color: inherit !important; }
.stTabs [data-baseweb="tab-panel"] { padding-top: 24px !important; }

/* Buttons */
.stButton > button[kind="primary"] {
    background: var(--red) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 2px !important;
    padding: 10px 28px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.7rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    transition: background 0.15s !important;
}
.stButton > button[kind="primary"]:hover { background: var(--red-dark) !important; }

/* Download buttons */
.stDownloadButton > button {
    border: 1.5px solid var(--red) !important;
    color: var(--red) !important;
    background: transparent !important;
    border-radius: 2px !important;
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    transition: all 0.15s !important;
}
.stDownloadButton > button:hover {
    background: var(--red) !important;
    color: white !important;
}

/* Radio */
.stRadio label, .stRadio p {
    font-family: var(--font-sans) !important;
    font-size: 0.88rem !important;
    color: var(--ink) !important;
    font-weight: 400 !important;
}

/* Text area */
.stTextArea textarea {
    font-family: var(--font-mono) !important;
    font-size: 0.82rem !important;
    border: 1px solid var(--rule) !important;
    border-radius: 2px !important;
    background: var(--surface) !important;
    color: var(--ink) !important;
}

/* Expanders */
[data-testid="stExpander"] {
    border: 1px solid var(--rule) !important;
    border-radius: 2px !important;
    background: var(--surface) !important;
}
details summary, .streamlit-expanderHeader,
[data-testid="stExpander"] summary {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.12em !important;
    color: var(--muted) !important;
    background: var(--surface) !important;
    padding: 12px 16px !important;
}

/* Status / alerts */
[data-testid="stStatus"] { border-radius: 2px !important; }
[data-testid="stAlert"] { border-radius: 2px !important; }

/* Dataframe */
.stDataFrame {
    border: 1px solid var(--rule) !important;
    border-radius: 2px !important;
}

/* Caption */
.stCaption p {
    font-family: var(--font-mono) !important;
    font-size: 0.68rem !important;
    color: var(--muted) !important;
}

/* Markdown text */
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: var(--ink) !important;
    font-family: var(--font-sans) !important;
}

/* Status spinner dots */
[data-testid="stStatus"] p,
[data-testid="stStatus"] span { color: var(--ink) !important; }
</style>
""", unsafe_allow_html=True)


# ── Masthead ──────────────────────────────────────────────────────────────────

st.markdown("""
<div class="lf-flag">
    <div class="lf-flag-inner">
        <div class="lf-flag-accent"></div>
        <div class="lf-flag-content">
            <div class="lf-flag-left">
                <div class="lf-flag-kicker">University of Cincinnati &nbsp;·&nbsp; Kautz-Uible Economics Institute</div>
                <div class="lf-flag-title">LaborFlex</div>
                <div class="lf-flag-sub">
                    Bureau of Labor Statistics &nbsp;·&nbsp; O*NET Web Services &nbsp;·&nbsp;
                    AI Analysis: Anthropic Claude &nbsp;·&nbsp; March 2026
                </div>
            </div>
            <div class="lf-flag-right">
                <div class="lf-flag-date">Vol. I &nbsp;·&nbsp; Issue 1</div>
                <span class="lf-flag-badge">Live Intelligence</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── Helpers ───────────────────────────────────────────────────────────────────

def run_with_logs(fn):
    buf = io.StringIO()
    with redirect_stdout(buf):
        result = fn()
    return result, buf.getvalue()


def rule(title: str):
    st.markdown(
        f'<div class="lf-rule">'
        f'<span class="lf-rule-text">{title}</span>'
        f'<span class="lf-rule-line"></span>'
        f'</div>',
        unsafe_allow_html=True,
    )


def kpi(label, value, sub="", css=""):
    return (
        f'<div class="lf-kpi {css}">'
        f'<div class="lf-kpi-label">{label}</div>'
        f'<div class="lf-kpi-value">{value}</div>'
        + (f'<div class="lf-kpi-sub">{sub}</div>' if sub else '')
        + '</div>'
    )


def download_row(outputs: dict):
    xl, pdf = outputs.get("excel"), outputs.get("pdf")
    c1, c2, _, _ = st.columns([1, 1, 2, 2])
    if xl and Path(xl).exists():
        with open(xl, "rb") as f:
            c1.download_button(
                "↓ Excel Dashboard", f,
                file_name=Path(xl).name,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )
    if pdf and Path(pdf).exists():
        with open(pdf, "rb") as f:
            c2.download_button(
                "↓ PDF Briefing", f,
                file_name=Path(pdf).name,
                mime="application/pdf",
                use_container_width=True,
            )


RISK_COLOR = {
    "CRITICAL": "#DC2626", "HIGH": "#EA580C",
    "MEDIUM": "#CA8A04",   "LOW": "#16A34A", "SAFE": "#2563EB",
}
RISK_EMOJI = {
    "CRITICAL": "🔴", "HIGH": "🟠", "MEDIUM": "🟡", "LOW": "🟢", "SAFE": "🔵",
}


# ══════════════════════════════════════════════════════════════════════════════
#  TABS
# ══════════════════════════════════════════════════════════════════════════════

tab1, tab2 = st.tabs(["Labor Market Analysis", "Automation Risk Analysis"])


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 1 — Labor Market Analysis
# ══════════════════════════════════════════════════════════════════════════════

with tab1:
    st.markdown("""
    <div class="lf-about">
        <div class="lf-about-icon">📡</div>
        <div class="lf-about-text">
            <strong>Labor Market Intelligence Pipeline</strong> — Collects real-time data from the
            Bureau of Labor Statistics Public Data API and O*NET Web Services, then applies AI economic
            analysis to produce institutional-grade labor market intelligence in Excel and PDF formats.
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Run Labor Market Analysis", type="primary", key="run_lm"):
        with st.status("Running intelligence pipeline...", expanded=True) as status:
            try:
                st.write("Step 1 — Collecting BLS + O*NET data...")
                from agents.labor_data_agent import LaborDataAgent
                data, logs1 = run_with_logs(LaborDataAgent().collect_all_data)

                st.write("Step 2 — Running AI economic analysis...")
                from agents.economic_analysis_agent import EconomicAnalysisAgent
                insights, logs2 = run_with_logs(
                    lambda: EconomicAnalysisAgent().run_full_analysis(data)
                )

                st.write("Step 3 — Generating Excel + PDF reports...")
                from agents.report_agent import ReportAgent
                outputs, logs3 = run_with_logs(
                    lambda: ReportAgent().generate_reports(
                        insights=insights,
                        csv_datasets=data.get("csv_datasets", {}),
                    )
                )

                st.session_state["lm_insights"] = insights
                st.session_state["lm_outputs"]  = outputs
                st.session_state["lm_logs"]     = logs1 + logs2 + logs3
                status.update(label="Intelligence report ready.", state="complete")

            except Exception as e:
                status.update(label="Pipeline error", state="error")
                st.error(str(e))

    if "lm_insights" in st.session_state:
        insights = st.session_state["lm_insights"]
        outputs  = st.session_state["lm_outputs"]
        u = insights.get("unemployment", {})
        w = insights.get("wages", {})
        p = insights.get("policy_structural", {})

        rule("Key Indicators")
        st.markdown(
            '<div class="lf-kpi-row lf-kpi-row-4">'
            + kpi("Unemployment Trend",  u.get("trend_direction", "—"))
            + kpi("Wage Trend",          w.get("overall_wage_trend", "—"))
            + kpi("Structural Signal",   p.get("structural_shift", "—"))
            + kpi("Analysis Confidence", p.get("confidence_level", "—"))
            + '</div>',
            unsafe_allow_html=True,
        )

        rule("Executive Summary")
        summary_html = "".join(
            f"<p>{para.strip()}</p>"
            for para in insights.get("executive_summary", "").split("\n\n")
            if para.strip()
        )
        st.markdown(f'<div class="lf-summary">{summary_html}</div>', unsafe_allow_html=True)

        rule("Findings")
        col_a, col_b = st.columns(2, gap="medium")

        with col_a:
            risks     = u.get("risk_factors", [])
            risk_html = "".join(f"<li>{r}</li>" for r in risks) or "<li>—</li>"
            st.markdown(f"""
            <div class="lf-card">
                <div class="lf-card-head">Unemployment Dynamics</div>
                <p><strong>Headline:</strong> {u.get('headline', '—')}</p>
                <p><strong>Key Finding:</strong> {u.get('key_finding', '—')}</p>
                <p><strong>Phillips Curve:</strong> {u.get('phillips_curve_signal', '—')}</p>
                <p><strong>Risk Factors:</strong></p><ul>{risk_html}</ul>
            </div>
            """, unsafe_allow_html=True)

        with col_b:
            leaders = ", ".join(w.get("sector_leaders", [])) or "—"
            st.markdown(f"""
            <div class="lf-card">
                <div class="lf-card-head">Wage Dynamics</div>
                <p><strong>Sector Leaders:</strong> {leaders}</p>
                <p><strong>Dispersion Signal:</strong> {w.get('wage_dispersion_signal', '—')}</p>
                <p><strong>Real Wage Status:</strong> {w.get('real_wage_assessment', '—')}</p>
                <p><strong>Policy Implication:</strong> {w.get('policy_implication', '—')}</p>
            </div>
            """, unsafe_allow_html=True)

        roles = ", ".join(p.get("high_demand_occupations", [])) or "—"
        st.markdown(f"""
        <div class="lf-card">
            <div class="lf-card-head">Structural Labor Market Analysis</div>
            <p><strong>High-Demand Occupations:</strong> {roles}</p>
            <p><strong>Automation Risk Signal:</strong> {p.get('automation_risk_signal', '—')}</p>
            <p><strong>Recommended Policy Focus:</strong> {p.get('recommended_policy_focus', '—')}</p>
        </div>
        """, unsafe_allow_html=True)

        rule("Export Reports")
        download_row(outputs)

        with st.expander("Pipeline Log"):
            st.code(st.session_state.get("lm_logs", ""), language="text")


# ══════════════════════════════════════════════════════════════════════════════
#  TAB 2 — Automation Risk Analysis
# ══════════════════════════════════════════════════════════════════════════════

with tab2:
    st.markdown("""
    <div class="lf-about">
        <div class="lf-about-icon">🤖</div>
        <div class="lf-about-text">
            <strong>Occupation Automation Risk Index</strong> — Evaluates each occupation across
            six dimensions: routinization, current AI capability, human interaction requirement,
            creativity, physical dexterity, and ethical judgment — using Claude and O*NET profiles.
        </div>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio(
        "Occupations to analyze",
        ["Default (16 occupations)", "Custom list"],
        horizontal=True,
    )

    custom_occs = None
    if mode == "Custom list":
        st.caption("One occupation per line — format: SOC_CODE | Job Title")
        raw = st.text_area(
            "Occupations",
            value=(
                "15-1252.00 | Software Developers\n"
                "29-1141.00 | Registered Nurses\n"
                "43-4051.00 | Customer Service Representatives\n"
                "53-3032.00 | Heavy and Tractor-Trailer Truck Drivers\n"
                "25-2021.00 | Elementary School Teachers"
            ),
            height=148,
            label_visibility="collapsed",
        )
        custom_occs = []
        for line in raw.strip().splitlines():
            if "|" in line:
                code, title = line.split("|", 1)
                custom_occs.append({"code": code.strip(), "title": title.strip()})
        if custom_occs:
            st.caption(f"{len(custom_occs)} occupation(s) queued.")
        else:
            st.warning("No valid occupations detected. Format: SOC_CODE | Job Title")

    if st.button("Run Automation Risk Analysis", type="primary", key="run_auto"):
        with st.status("Scoring occupations...", expanded=True) as status:
            try:
                st.write("Analyzing automation risk dimensions with Claude...")
                from agents.automation_risk_agent import AutomationRiskAgent
                analysis, logs1 = run_with_logs(
                    lambda: AutomationRiskAgent().run(occupations=custom_occs)
                )

                st.write("Generating Excel + PDF reports...")
                from agents.automation_report_agent import AutomationReportAgent
                outputs, logs2 = run_with_logs(
                    lambda: AutomationReportAgent().generate(analysis)
                )

                st.session_state["auto_analysis"] = analysis
                st.session_state["auto_outputs"]  = outputs
                st.session_state["auto_logs"]     = logs1 + logs2
                status.update(label="Risk index ready.", state="complete")

            except Exception as e:
                status.update(label="Pipeline error", state="error")
                st.error(str(e))

    if "auto_analysis" in st.session_state:
        analysis = st.session_state["auto_analysis"]
        outputs  = st.session_state["auto_outputs"]
        meta     = analysis.get("metadata", {})
        results  = analysis.get("results", [])
        policy   = analysis.get("policy_report", {})
        dist     = meta.get("distribution", {})
        sorted_r = sorted(results, key=lambda x: x["automation_score"], reverse=True)

        # ── Risk summary KPIs ─────────────────────────────────────────────────
        rule("Risk Summary")
        low_safe = dist.get("LOW", 0) + dist.get("SAFE", 0)
        st.markdown(
            '<div class="lf-kpi-row lf-kpi-row-5">'
            + kpi("Avg Risk Score", f"{meta.get('average_score', 0):.1f}",
                  sub="out of 100")
            + kpi("Critical",  str(dist.get("CRITICAL", 0)), sub="occupations", css="r-critical")
            + kpi("High",      str(dist.get("HIGH",     0)), sub="occupations", css="r-high")
            + kpi("Medium",    str(dist.get("MEDIUM",   0)), sub="occupations", css="r-medium")
            + kpi("Low / Safe", str(low_safe),               sub="occupations", css="r-low")
            + '</div>',
            unsafe_allow_html=True,
        )

        # ── Distribution bar ──────────────────────────────────────────────────
        total = len(results) or 1
        bar_segs = "".join(
            f'<div style="flex:{dist.get(lvl,0)/total*100};'
            f'background:{RISK_COLOR[lvl]};height:100%" '
            f'title="{lvl}: {dist.get(lvl,0)}"></div>'
            for lvl in ["CRITICAL","HIGH","MEDIUM","LOW","SAFE"]
        )
        st.markdown(
            f'<div style="display:flex;height:6px;gap:2px;margin:-8px 0 20px;'
            f'border-radius:1px;overflow:hidden">{bar_segs}</div>',
            unsafe_allow_html=True,
        )

        # ── Occupation rankings ───────────────────────────────────────────────
        rule("Occupation Risk Rankings")
        for r in sorted_r:
            lvl   = r["risk_level"]
            score = r["automation_score"]
            color = RISK_COLOR.get(lvl, "#94A3B8")
            st.markdown(f"""
            <div class="lf-occ-card">
                <div class="lf-occ-header">
                    <span class="lf-occ-title">{r['title']}</span>
                    <span class="lf-occ-score" style="color:{color}">{score:.0f}<span style="font-size:0.7em;color:#94A3B8">/100</span></span>
                </div>
                <div class="lf-score-bar-bg">
                    <div class="lf-score-bar" style="width:{score}%;background:{color}"></div>
                </div>
                <div class="lf-occ-meta">
                    <span class="lf-tag lf-tag-{lvl}">{lvl}</span>
                    <span class="lf-tag-detail">⏱ {r.get('time_horizon','—')}</span>
                    <span class="lf-tag-detail">·</span>
                    <span class="lf-tag-detail">{r.get('reasoning','')[:110]}{'…' if len(r.get('reasoning',''))>110 else ''}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # ── Detailed breakdown ────────────────────────────────────────────────
        rule("Detailed Analysis")
        with st.expander("View full occupation breakdown"):
            for r in sorted_r:
                lvl   = r["risk_level"]
                color = RISK_COLOR.get(lvl, "#94A3B8")
                tasks = "; ".join(r.get("tasks_at_risk", [])) or "—"
                techs = "; ".join(r.get("threatening_technologies", [])) or "—"
                resil = "; ".join(r.get("resilient_tasks", [])) or "—"
                st.markdown(f"""
                <div class="lf-card" style="border-left:3px solid {color};margin-bottom:12px">
                    <div class="lf-card-head"
                         style="display:flex;justify-content:space-between;align-items:center">
                        <span>{r['title']}</span>
                        <span class="lf-tag lf-tag-{lvl}">{lvl} · {r['automation_score']:.0f}/100</span>
                    </div>
                    <p style="color:#64748B;font-size:0.84rem;margin-bottom:12px;font-style:italic">
                        {r.get('reasoning', '')}
                    </p>
                    <p><strong>Tasks at risk:</strong> {tasks}</p>
                    <p><strong>Threatening technologies:</strong> {techs}</p>
                    <p><strong>Resilient tasks:</strong> {resil}</p>
                    <p><strong>Worker recommendation:</strong> {r.get('worker_recommendation','')}</p>
                    <p><strong>Policy recommendation:</strong> {r.get('policy_recommendation','')}</p>
                </div>
                """, unsafe_allow_html=True)

        # ── Policy report ─────────────────────────────────────────────────────
        rule("Policy Report")

        # Diagnosis strip
        urgency_color = {"HIGH": "#DC2626", "MEDIUM": "#CA8A04", "LOW": "#16A34A"}.get(
            policy.get("policy_urgency",""), "#6B7280"
        )
        st.markdown(f"""
        <div class="lf-card" style="margin-bottom:14px">
            <div class="lf-card-head"
                 style="display:flex;justify-content:space-between;align-items:center">
                <span>Overall Diagnosis</span>
                <span style="font-family:var(--font-mono);font-size:0.62rem;
                             color:{urgency_color};letter-spacing:0.1em">
                    ● URGENCY: {policy.get('policy_urgency','—')}
                </span>
            </div>
            <p>{policy.get('overall_diagnosis', '—')}</p>
        </div>
        """, unsafe_allow_html=True)

        # Policy cards
        policies = policy.get("priority_policies", [])
        cards_html = ""
        for i, pol in enumerate(policies):
            cards_html += f"""
            <div class="lf-policy-card">
                <div class="lf-policy-num">Policy 0{i+1}</div>
                <div class="lf-policy-name">{pol.get('name','')}</div>
                <div class="lf-policy-desc">{pol.get('description','')}</div>
                <div class="lf-policy-chips">
                    <span class="lf-chip">{pol.get('horizon','')}</span>
                    <span class="lf-chip">{pol.get('target_population','')}</span>
                </div>
            </div>"""

        st.markdown(f'<div class="lf-policy-grid">{cards_html}</div>', unsafe_allow_html=True)

        # Indicators + key message
        indicators = policy.get("monitoring_indicators", [])
        if indicators:
            ind_html = " &nbsp;·&nbsp; ".join(
                f'<span style="font-family:var(--font-mono);font-size:0.72rem;color:var(--muted)">{ind}</span>'
                for ind in indicators
            )
            st.markdown(
                f'<div style="background:var(--surface-2);border:1px solid var(--rule);'
                f'padding:12px 16px;margin-bottom:12px">'
                f'<span style="font-family:var(--font-mono);font-size:0.6rem;'
                f'letter-spacing:0.16em;text-transform:uppercase;color:var(--red)">'
                f'Monitoring Indicators &nbsp; </span>{ind_html}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(f"""
        <div class="lf-dispatch">
            <div class="lf-dispatch-label">Key Message</div>
            <div class="lf-dispatch-text">{policy.get('key_message', '')}</div>
        </div>
        """, unsafe_allow_html=True)

        rule("Export Reports")
        download_row(outputs)

        with st.expander("Pipeline Log"):
            st.code(st.session_state.get("auto_logs", ""), language="text")