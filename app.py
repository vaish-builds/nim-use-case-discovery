import streamlit as st
from openai import OpenAI
import json

st.set_page_config(
    page_title="NIM Use Case Discovery Engine",
    page_icon="🔍",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
  font-family: 'Inter', sans-serif !important;
  background-color: #f7f8fa !important;
  color: #111827 !important;
}

/* Force light mode on all streamlit containers */
.stApp {
  background-color: #f7f8fa !important;
}
.block-container {
  background-color: #f7f8fa !important;
  padding-top: 0.2rem !important;
}
[data-testid="stAppViewContainer"] {
  background-color: #f7f8fa !important;
}
[data-testid="stHeader"] {
  background-color: #f7f8fa !important;
}

#MainMenu, footer, header { visibility: hidden; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 4px; }

/* Top navigation */
.navbar {
  display: flex; align-items: center; justify-content: space-between;
  padding: 8px 0 12px 0;
  border-bottom: 1px solid #e5e7eb;
  margin-bottom: 20px;
}
.navbar-left { display: flex; align-items: center; gap: 14px; }
.nvidia-mark { font-size: 16px; font-weight: 800; letter-spacing: 2px; color: #76b900; }
.nav-pipe { width: 1px; height: 22px; background: #e5e7eb; }
.nav-title { font-size: 15px; color: #374151; font-weight: 500; }
.nav-badge {
  font-size: 10px; font-weight: 600; letter-spacing: 0.8px;
  color: #76b900; border: 1px solid #76b900;
  padding: 4px 10px; border-radius: 20px;
  background: #f0fdf4;
}

/* Hero section */
.hero {
  text-align: center;
  padding: 16px 0 20px 0;
  max-width: 680px;
  margin: 0 auto 28px auto;
}
.hero-tag {
  display: inline-block;
  font-size: 11px; font-weight: 600; letter-spacing: 1.2px;
  color: #76b900; text-transform: uppercase;
  background: #f0fdf4; border: 1px solid #bbf7d0;
  padding: 5px 14px; border-radius: 20px;
  margin-bottom: 20px;
}
.hero-title {
  font-size: 36px; font-weight: 700; color: #111827;
  line-height: 1.25; margin-bottom: 16px; letter-spacing: -0.5px;
}
.hero-title span { color: #76b900; }
.hero-sub {
  font-size: 15px; color: #6b7280; line-height: 1.75;
}

/* Step cards */
.step-wrap {
  display: flex; align-items: center; gap: 8px; margin-bottom: 10px;
}
.step-num {
  width: 24px; height: 24px; border-radius: 50%;
  background: #76b900; color: white;
  font-size: 11px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.step-label { font-size: 13px; font-weight: 600; color: #374151; }

/* Input card */
.input-card {
  background: white;
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 28px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* Selection pills */
.pill-grid {
  display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px;
}
.pill {
  padding: 7px 14px; border-radius: 20px; font-size: 12px; font-weight: 500;
  border: 1.5px solid #e5e7eb; background: white; color: #6b7280;
  cursor: pointer; transition: all 0.15s;
}
.pill:hover { border-color: #76b900; color: #76b900; background: #f0fdf4; }
.pill.selected { border-color: #76b900; color: #76b900; background: #f0fdf4; font-weight: 600; }

/* Run button */
.stButton > button {
  background: #76b900 !important; color: white !important;
  font-weight: 600 !important; border: none !important;
  border-radius: 10px !important; padding: 14px 0 !important;
  font-size: 14px !important; width: 100% !important;
  letter-spacing: 0.3px !important;
  box-shadow: 0 4px 14px rgba(118,185,0,0.3) !important;
  transition: all 0.2s !important;
}
.stButton > button:hover {
  background: #65a000 !important;
  box-shadow: 0 6px 20px rgba(118,185,0,0.4) !important;
  transform: translateY(-1px) !important;
}

/* Result card */
.result-card {
  background: white; border: 1px solid #e5e7eb;
  border-radius: 16px; padding: 28px;
  margin-bottom: 16px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}
.result-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 24px; padding-bottom: 16px;
  border-bottom: 1px solid #f3f4f6;
}
.result-title { font-size: 16px; font-weight: 700; color: #111827; }
.result-meta { font-size: 12px; color: #9ca3af; }

/* Use case card */
.uc-card {
  background: #fafafa; border: 1px solid #f3f4f6;
  border-radius: 12px; padding: 20px;
  margin-bottom: 12px;
  transition: box-shadow 0.2s;
}
.uc-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.06); }
.uc-card-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 10px;
}
.uc-rank {
  width: 28px; height: 28px; border-radius: 8px;
  background: #76b900; color: white;
  font-size: 13px; font-weight: 700;
  display: flex; align-items: center; justify-content: center;
}
.uc-badges { display: flex; gap: 6px; }
.uc-badge {
  font-size: 10px; font-weight: 600; padding: 3px 9px;
  border-radius: 20px; letter-spacing: 0.3px;
}
.badge-high { background: #dcfce7; color: #166534; }
.badge-med { background: #fef9c3; color: #854d0e; }
.badge-low { background: #fee2e2; color: #991b1b; }
.badge-effort-low { background: #ede9fe; color: #5b21b6; }
.badge-effort-med { background: #e0f2fe; color: #075985; }
.badge-effort-high { background: #fff7ed; color: #9a3412; }
.uc-title { font-size: 14px; font-weight: 600; color: #111827; margin-bottom: 6px; }
.uc-desc { font-size: 13px; color: #6b7280; line-height: 1.65; margin-bottom: 10px; }
.uc-footer {
  display: flex; align-items: center; gap: 16px;
  font-size: 11px; color: #9ca3af;
  padding-top: 10px; border-top: 1px solid #f3f4f6;
}
.uc-footer span { display: flex; align-items: center; gap: 4px; }

/* Score bar */
.score-row { margin-bottom: 8px; }
.score-label {
  display: flex; justify-content: space-between;
  font-size: 11px; color: #9ca3af; margin-bottom: 3px;
}
.score-bar-bg {
  background: #f3f4f6; border-radius: 4px; height: 5px; overflow: hidden;
}
.score-bar-fill { height: 5px; border-radius: 4px; background: #76b900; }

/* Summary box */
.summary-box {
  background: linear-gradient(135deg, #f0fdf4 0%, #f8f9fb 100%);
  border: 1px solid #bbf7d0; border-radius: 12px;
  padding: 20px; margin-top: 16px;
}
.summary-title { font-size: 13px; font-weight: 600; color: #166534; margin-bottom: 8px; }
.summary-text { font-size: 12px; color: #374151; line-height: 1.7; }

/* Stat pills row */
.stat-row { display: flex; gap: 10px; margin-bottom: 24px; }
.stat-pill {
  flex: 1; background: #f8f9fb; border: 1px solid #e5e7eb;
  border-radius: 10px; padding: 14px 16px; text-align: center;
}
.stat-val { font-size: 22px; font-weight: 700; color: #76b900; }
.stat-label { font-size: 11px; color: #9ca3af; margin-top: 2px; }

/* Sidebar */
[data-testid="stSidebar"] {
  background: white !important;
  border-right: 1px solid #e5e7eb !important;
}

/* Streamlit overrides */
.stTextInput input {
  background: #f8f9fb !important; border: 1.5px solid #e5e7eb !important;
  border-radius: 10px !important; color: #374151 !important;
  font-size: 13px !important; padding: 10px 14px !important;
}
.stTextInput input:focus { border-color: #76b900 !important; }
.stTextArea textarea {
  background: #f8f9fb !important;
  border: 1.5px solid #e5e7eb !important;
  border-radius: 10px !important;
  color: #374151 !important;
  font-size: 13px !important;
  padding: 10px 14px !important;
  resize: none !important;
}
.stTextArea textarea:focus { border-color: #76b900 !important; outline: none !important; box-shadow: none !important; }
.stTextArea textarea::placeholder { color: #9ca3af !important; font-size: 13px !important; }
.stSelectbox > div > div {
  background: #f8f9fb !important; border: 1.5px solid #e5e7eb !important;
  border-radius: 10px !important; color: #374151 !important;
}
.stMultiSelect > div > div {
  background: #f8f9fb !important; border: 1.5px solid #e5e7eb !important;
  border-radius: 10px !important; color: #374151 !important;
}
.stMultiSelect > div > div > div {
  background: #f8f9fb !important; color: #374151 !important;
}
/* Selected tags in multiselect */
.stMultiSelect span[data-baseweb="tag"] {
  background: #f0fdf4 !important; color: #166534 !important;
  border: 1px solid #86efac !important;
}
/* Dropdown menu */
ul[data-baseweb="menu"] {
  background: white !important; border: 1px solid #e5e7eb !important;
}
li[role="option"] {
  color: #374151 !important; background: white !important;
}
li[role="option"]:hover {
  background: #f0fdf4 !important;
}
/* Text inside multiselect input */
.stMultiSelect input {
  color: #374151 !important; background: transparent !important;
}
.stSlider > div > div > div { background: #76b900 !important; }
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] {
  color: #374151 !important; font-size: 11px !important; font-weight: 600 !important;
}
div[data-baseweb="slider"] span { color: #374151 !important; }
.stDownloadButton > button {
  background: white !important; color: #76b900 !important;
  border: 1.5px solid #76b900 !important; border-radius: 10px !important;
  font-size: 13px !important; font-weight: 500 !important;
  width: 100% !important;
}
.stDownloadButton > button:hover {
  background: #f0fdf4 !important;
}
div[data-testid="stExpander"] {
  background: white !important; border: 1px solid #e5e7eb !important;
  border-radius: 12px !important;
}
.stSpinner > div { border-top-color: #76b900 !important; }
</style>
""", unsafe_allow_html=True)

# ── Navbar ────────────────────────────────────────────────────
st.markdown("""
<div class="navbar">
  <div class="navbar-left">
    <div class="nvidia-mark">NVIDIA</div>
    <div class="nav-pipe"></div>
    <div class="nav-title">NIM Use Case Discovery Engine</div>
  </div>
  <div class="nav-badge">POWERED BY NIM</div>
</div>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding: 8px 0 20px 0;">
      <div style="font-size:11px; font-weight:600; letter-spacing:1.2px; color:#9ca3af; text-transform:uppercase; margin-bottom:12px;">Configuration</div>
    </div>
    """, unsafe_allow_html=True)

    api_key = st.text_input("NVIDIA NIM API Key", type="password", placeholder="nvapi-...")
    st.caption("Free key at build.nvidia.com")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px; font-weight:600; letter-spacing:1.2px; color:#9ca3af; text-transform:uppercase; margin-bottom:8px;">NIM Model</div>', unsafe_allow_html=True)
    model = st.selectbox("Model", [
        "meta/llama-3.1-70b-instruct",
        "mistralai/mistral-7b-instruct-v0.3",
        "microsoft/phi-3-mini-128k-instruct",
    ], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#f8f9fb; border:1px solid #e5e7eb; border-radius:10px; padding:16px;">
      <div style="font-size:12px; font-weight:600; color:#374151; margin-bottom:8px;">How it works</div>
      <div style="font-size:11px; color:#6b7280; line-height:1.7;">
        1. Describe your enterprise context<br>
        2. Select your industry and challenges<br>
        3. NIM generates your top AI use cases<br>
        4. Get a prioritized roadmap + exec summary
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.caption("Built by Vaishnavi Awasthi · MEM @ Duke")

# ── Hero ──────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-tag">Enterprise AI Adoption · Powered by NVIDIA NIM</div>
  <div class="hero-title">Discover where <span>AI can transform</span><br>your enterprise</div>
  <div class="hero-sub">Answer a few questions about your organization. NIM will identify your highest-impact AI use cases and generate a prioritized implementation roadmap — ready to share with leadership.</div>
</div>
""", unsafe_allow_html=True)

# ── Main form ─────────────────────────────────────────────────
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="step-wrap">
      <div class="step-num">1</div>
      <div class="step-label">Your Organization</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px; color:#6b7280; margin-bottom:6px;">Industry</div>', unsafe_allow_html=True)
    industry = st.selectbox("Industry", [
        "Select your industry...",
        "Financial Services & Banking",
        "Healthcare & Life Sciences",
        "Retail & E-commerce",
        "Manufacturing & Supply Chain",
        "Government & Defense",
        "Energy & Utilities",
        "Telecommunications",
        "Media & Entertainment",
        "Education & Research",
        "Insurance",
    ], label_visibility="collapsed")

    st.markdown('<div style="font-size:12px; color:#6b7280; margin-bottom:6px;">Organization size</div>', unsafe_allow_html=True)
    org_size = st.selectbox("Organization size", [
        "Select organization size...",
        "Small (< 500 employees)",
        "Mid-market (500–5,000 employees)",
        "Enterprise (5,000–50,000 employees)",
        "Large Enterprise (50,000+ employees)",
    ], label_visibility="collapsed")

    st.markdown('<div style="font-size:12px; color:#6b7280; margin-bottom:6px;">AI / Technical maturity</div>', unsafe_allow_html=True)
    tech_maturity = st.selectbox("AI maturity", [
        "Select maturity level...",
        "Beginner — No AI experience yet",
        "Developing — Exploring AI tools",
        "Intermediate — Some AI pilots running",
        "Advanced — AI in production",
        "Leading — AI-first organization",
    ], index=0, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div class="step-wrap">
      <div class="step-num">2</div>
      <div class="step-label">Current Challenges</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px; color:#6b7280; margin-bottom:6px;">Select your top challenges <span style="color:#9ca3af;">(pick up to 4)</span></div>', unsafe_allow_html=True)
    challenges = st.multiselect(
        "Select your top challenges (pick up to 4)",
        [
            "High operational costs",
            "Slow manual processes",
            "Poor customer experience",
            "Data silos and poor insights",
            "Talent shortage",
            "Compliance and risk management",
            "Slow product development cycles",
            "Cybersecurity threats",
            "Supply chain inefficiencies",
            "Low employee productivity",
        ],
        max_selections=4,
        label_visibility="collapsed",
        placeholder="Select challenges..."
    )

with col2:
    st.markdown("""
    <div class="step-wrap">
      <div class="step-num">3</div>
      <div class="step-label">Priorities & Constraints</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div style="font-size:12px; color:#6b7280; margin-bottom:6px;">Primary business goal</div>', unsafe_allow_html=True)
    primary_goal = st.selectbox("Primary business goal", [
        "Select primary goal...",
        "Reduce operational costs",
        "Improve customer experience",
        "Accelerate product development",
        "Enhance decision making",
        "Improve employee productivity",
        "Strengthen security and compliance",
        "Enter new markets",
    ], label_visibility="collapsed")

    st.markdown('<div style="font-size:12px; color:#6b7280; margin-bottom:6px;">AI investment budget</div>', unsafe_allow_html=True)
    budget = st.selectbox("AI investment budget", [
        "Select budget range...",
        "Exploring (< $100K)",
        "Pilot stage ($100K – $500K)",
        "Scaling ($500K – $2M)",
        "Full deployment ($2M+)",
    ], label_visibility="collapsed")

    st.markdown('<div style="font-size:12px; color:#6b7280; margin-bottom:6px;">Implementation timeline</div>', unsafe_allow_html=True)
    timeline = st.selectbox("Implementation timeline", [
        "Select timeline...",
        "Quick wins (0–3 months)",
        "Short term (3–6 months)",
        "Medium term (6–12 months)",
        "Long term (12+ months)",
    ], label_visibility="collapsed")

    st.markdown('<div style="font-size:12px; color:#6b7280; margin-bottom:6px;">Additional context <span style="color:#d1d5db;">(optional)</span></div>', unsafe_allow_html=True)
    additional = st.text_area(
        "Additional context",
        placeholder="e.g. We process 10,000 support tickets daily. We use Salesforce and Snowflake.",
        height=122,
        label_visibility="collapsed"
    )

    discover_btn = False

# ── Centered button ──────────────────────────────────────────
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    discover_btn = st.button("Discover My AI Use Cases", use_container_width=True)

# ── Results ───────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if discover_btn:
    if not api_key:
        st.error("Please enter your NVIDIA NIM API key in the sidebar.")
        st.stop()
    if not challenges:
        st.error("Please select at least one challenge.")
        st.stop()

    st.markdown("""
    <div style="background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:16px 20px; margin-bottom:16px; text-align:center;">
      <div style="font-size:13px; font-weight:600; color:#166534; margin-bottom:4px;">⚡ NIM is generating your use case roadmap</div>
      <div style="font-size:12px; color:#4ade80;">Making live API calls to NVIDIA NIM · This takes 30–60 seconds</div>
    </div>
    """, unsafe_allow_html=True)
    with st.spinner("Analyzing your enterprise context across 5 AI opportunity dimensions..."):
        try:
            client = OpenAI(
                base_url="https://integrate.api.nvidia.com/v1",
                api_key=api_key
            )

            prompt = f"""You are a Senior Enterprise AI Strategist at NVIDIA, helping enterprises identify their highest-impact AI use cases using NVIDIA NIM inference microservices.

Enterprise Context:
- Industry: {industry}
- Organization Size: {org_size}
- AI/Technical Maturity: {tech_maturity}
- Primary Business Goal: {primary_goal}
- Investment Budget: {budget}
- Implementation Timeline: {timeline}
- Top Challenges: {', '.join(challenges) if challenges else 'Not specified'}
- Additional Context: {additional if additional else 'None provided'}

Generate exactly 5 AI use cases tailored to this enterprise. For each use case, provide:

1. A specific, concrete use case title (not generic)
2. A 2-3 sentence description of what it does and how NIM enables it
3. Business impact score (1-10)
4. Implementation effort: Low / Medium / High
5. Time to value: Quick Win (0-3 months) / Short Term (3-6 months) / Medium Term (6-12 months)
6. Key metric it improves (one specific KPI with estimated improvement %)
7. Which NVIDIA NIM model is best suited: Llama 3.1 70B / Mistral 7B / Phi-3 Mini — and why in one sentence

Then provide:
- A 3-sentence executive summary suitable for a C-suite presentation
- One sentence on why NVIDIA NIM is the right infrastructure choice for this enterprise

Format your response as valid JSON only, no markdown, no backticks, exactly this structure:
{{
  "use_cases": [
    {{
      "rank": 1,
      "title": "",
      "description": "",
      "impact_score": 0,
      "effort": "",
      "time_to_value": "",
      "kpi": "",
      "kpi_improvement": "",
      "recommended_model": "",
      "model_reason": ""
    }}
  ],
  "executive_summary": "",
  "nim_rationale": ""
}}"""

            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are an enterprise AI strategist. Always respond with valid JSON only. No markdown, no backticks, no extra text."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=2000,
                temperature=0.4
            )

            raw = response.choices[0].message.content.strip()
            # Clean any accidental markdown
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            if raw.endswith("```"):
                raw = raw[:-3]

            data = json.loads(raw.strip())
            use_cases = data.get("use_cases", [])
            exec_summary = data.get("executive_summary", "")
            nim_rationale = data.get("nim_rationale", "")

            # ── Stats row ─────────────────────────────────────
            avg_impact = round(sum(uc.get("impact_score", 0) for uc in use_cases) / len(use_cases), 1) if use_cases else 0
            quick_wins = sum(1 for uc in use_cases if "Quick" in uc.get("time_to_value", ""))

            st.markdown(f"""
            <div class="stat-row">
              <div class="stat-pill">
                <div class="stat-val">{len(use_cases)}</div>
                <div class="stat-label">Use cases identified</div>
              </div>
              <div class="stat-pill">
                <div class="stat-val">{avg_impact}/10</div>
                <div class="stat-label">Avg business impact</div>
              </div>
              <div class="stat-pill">
                <div class="stat-val">{quick_wins}</div>
                <div class="stat-label">Quick wins (0–3 mo)</div>
              </div>
              <div class="stat-pill">
                <div class="stat-val" style="font-size:13px; font-weight:700; line-height:1.3;">{industry.split('&')[0].strip()[:16]}</div>
                <div class="stat-label">Industry context</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Use case cards ────────────────────────────────
            st.markdown('<div style="font-size:11px; font-weight:600; letter-spacing:1.2px; color:#9ca3af; text-transform:uppercase; margin-bottom:16px;">Prioritized Use Cases</div>', unsafe_allow_html=True)

            for uc in use_cases:
                impact = uc.get("impact_score", 0)
                effort = uc.get("effort", "Medium")
                ttv = uc.get("time_to_value", "")
                model_short = uc.get("recommended_model", "").split("/")[-1]

                impact_class = "badge-high" if impact >= 8 else ("badge-med" if impact >= 6 else "badge-low")
                effort_class = "badge-effort-low" if effort == "Low" else ("badge-effort-med" if effort == "Medium" else "badge-effort-high")
                bar_width = impact * 10
                impact_color = "#16a34a" if impact >= 8 else ("#ca8a04" if impact >= 6 else "#dc2626")

                st.markdown(f"""
                <div class="uc-card">
                  <div style="display:flex; align-items:center; gap:12px; margin-bottom:14px;">
                    <div class="uc-rank">#{uc.get('rank', '')}</div>
                    <div style="flex:1;">
                      <div class="uc-title" style="margin-bottom:0;">{uc.get('title', '')}</div>
                    </div>
                    <div class="uc-badges">
                      <span class="uc-badge {impact_class}">Impact {impact}/10</span>
                      <span class="uc-badge {effort_class}">{effort} effort</span>
                    </div>
                  </div>
                  <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-bottom:14px;">
                    <div style="background:#f8f9fb; border-radius:8px; padding:10px 12px;">
                      <div style="font-size:10px; color:#9ca3af; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:4px;">Timeline</div>
                      <div style="font-size:12px; font-weight:600; color:#374151;">{ttv}</div>
                    </div>
                    <div style="background:#f8f9fb; border-radius:8px; padding:10px 12px;">
                      <div style="font-size:10px; color:#9ca3af; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:4px;">KPI Impact</div>
                      <div style="font-size:12px; font-weight:600; color:{impact_color};">{uc.get('kpi_improvement', '')} ↑ {uc.get('kpi', '')}</div>
                    </div>
                    <div style="background:#f8f9fb; border-radius:8px; padding:10px 12px;">
                      <div style="font-size:10px; color:#9ca3af; text-transform:uppercase; letter-spacing:0.8px; margin-bottom:4px;">NIM Model</div>
                      <div style="font-size:12px; font-weight:600; color:#374151;">{model_short[:16]}</div>
                    </div>
                  </div>
                  <div style="font-size:12px; color:#6b7280; line-height:1.65; padding-top:10px; border-top:1px solid #f3f4f6;">{uc.get('description', '')}</div>
                </div>
                """, unsafe_allow_html=True)

            # ── Executive summary ─────────────────────────────
            st.markdown(f"""
            <div style="background:linear-gradient(135deg, #f0fdf4 0%, #f7fee7 100%); border:1.5px solid #86efac; border-radius:14px; padding:28px; margin-top:20px;">
              <div style="display:flex; align-items:center; gap:10px; margin-bottom:16px;">
                <div style="width:32px; height:32px; background:#76b900; border-radius:8px; display:flex; align-items:center; justify-content:center; color:white; font-size:14px; font-weight:700;">C</div>
                <div>
                  <div style="font-size:13px; font-weight:700; color:#166534;">Executive Summary</div>
                  <div style="font-size:11px; color:#4ade80;">Ready to share with leadership</div>
                </div>
              </div>
              <div style="font-size:14px; color:#166534; line-height:1.8; margin-bottom:16px; font-weight:500;">{exec_summary}</div>
              <div style="background:white; border-radius:10px; padding:14px 16px; border:1px solid #bbf7d0;">
                <div style="font-size:10px; font-weight:600; color:#76b900; text-transform:uppercase; letter-spacing:1px; margin-bottom:6px;">Why NVIDIA NIM</div>
                <div style="font-size:13px; color:#374151; line-height:1.65;">{nim_rationale}</div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # ── Download ──────────────────────────────────────
            st.markdown("<br>", unsafe_allow_html=True)
            report_lines = [
                f"NIM USE CASE DISCOVERY REPORT",
                f"Industry: {industry} | Size: {org_size} | Maturity: {tech_maturity}",
                f"Generated via NVIDIA NIM · {model}",
                f"",
                f"EXECUTIVE SUMMARY",
                exec_summary,
                f"",
                f"WHY NVIDIA NIM",
                nim_rationale,
                f"",
                f"PRIORITIZED USE CASES",
            ]
            for uc in use_cases:
                report_lines += [
                    f"",
                    f"#{uc.get('rank')} {uc.get('title')}",
                    f"Impact: {uc.get('impact_score')}/10 | Effort: {uc.get('effort')} | Timeline: {uc.get('time_to_value')}",
                    f"KPI: {uc.get('kpi')} +{uc.get('kpi_improvement')}",
                    f"Recommended Model: {uc.get('recommended_model')}",
                    f"{uc.get('description')}",
                    f"Model rationale: {uc.get('model_reason')}",
                ]
            report_text = "\n".join(report_lines)

            st.download_button(
                "⬇️ Download Executive Report (.txt)",
                data=report_text,
                file_name="nim_use_case_discovery_report.txt",
                mime="text/plain",
                use_container_width=True
            )

        except json.JSONDecodeError:
            st.error("NIM returned an unexpected format. Please try again.")
            with st.expander("Raw response (for debugging)"):
                st.code(raw)
        except Exception as e:
            st.error(f"Error: {e}")
            st.info("Check your API key and ensure you have NIM credits at build.nvidia.com")

else:
    # Empty state
    st.markdown("""
    <div style="background:white; border:1px solid #e5e7eb; border-radius:16px; padding:48px; text-align:center; box-shadow:0 1px 3px rgba(0,0,0,0.04);">
      <div style="font-size:32px; margin-bottom:16px;">✦</div>
      <div style="font-size:16px; font-weight:600; color:#111827; margin-bottom:8px;">Your use case roadmap will appear here</div>
      <div style="font-size:13px; color:#9ca3af; line-height:1.7; max-width:420px; margin:0 auto;">
        Fill in your organization details on the left, select your top challenges, and click Discover. NIM will generate a prioritized AI adoption roadmap tailored to your enterprise in seconds.
      </div>
      <div style="display:flex; justify-content:center; gap:24px; margin-top:32px;">
        <div style="text-align:center;">
          <div style="font-size:20px; font-weight:700; color:#76b900;">5</div>
          <div style="font-size:11px; color:#9ca3af;">use cases generated</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:20px; font-weight:700; color:#76b900;">10+</div>
          <div style="font-size:11px; color:#9ca3af;">industries supported</div>
        </div>
        <div style="text-align:center;">
          <div style="font-size:20px; font-weight:700; color:#76b900;">3</div>
          <div style="font-size:11px; color:#9ca3af;">NIM models compared</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:48px; padding-top:20px; border-top:1px solid #e5e7eb; display:flex; justify-content:space-between; align-items:center;">
  <div style="font-size:11px; color:#d1d5db;">Built by Vaishnavi Awasthi · MEM @ Duke University</div>
  <div style="font-size:11px; color:#d1d5db;">NIM Use Case Discovery Engine · github.com/vaish-builds</div>
</div>
""", unsafe_allow_html=True)
