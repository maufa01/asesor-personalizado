"""
Configuración visual y CSS personalizado para FinanzasIA
Aesthetic: Luxury Dark Finance — inspired by Bloomberg terminals and premium trading platforms
"""

import streamlit as st


def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Cormorant+Garamond:wght@300;400;500;600&display=swap');

    /* ── Reset & Base ─────────────────────────────────────────────── */
    :root {
        --bg-0:       #050810;
        --bg-1:       #0b0f1a;
        --bg-2:       #111827;
        --bg-3:       #1a2235;
        --bg-card:    #0f1623;
        --border:     rgba(99,120,180,0.18);
        --border-glow:rgba(99,182,255,0.35);
        --gold:       #f0b429;
        --gold-dim:   #c99a1e;
        --green:      #10d98a;
        --green-dim:  #0bb074;
        --red:        #ff4d6a;
        --blue:       #4fa3ff;
        --blue-dim:   #2d7dcc;
        --text-1:     #eef2ff;
        --text-2:     #94a3b8;
        --text-3:     #64748b;
        --accent:     #4fa3ff;
        --font-display: 'Syne', sans-serif;
        --font-body:    'DM Sans', sans-serif;
        --font-numbers: 'Cormorant Garamond', Georgia, serif;
        --radius-sm:  8px;
        --radius-md:  14px;
        --radius-lg:  20px;
        --shadow-card: 0 4px 32px rgba(0,0,0,0.5), 0 1px 0 rgba(255,255,255,0.04) inset;
    }

    html, body, [class*="css"] {
        font-family: var(--font-body) !important;
        color: var(--text-1) !important;
        background-color: var(--bg-0) !important;
    }

    /* ── Hide Streamlit chrome ────────────────────────────────────── */
    #MainMenu, footer, header { visibility: hidden; }
    .stDeployButton { display: none; }
    .block-container {
        padding: 0 2rem 4rem !important;
        max-width: 1280px !important;
    }

    /* ── Scrollbar ────────────────────────────────────────────────── */
    ::-webkit-scrollbar { width: 6px; background: var(--bg-1); }
    ::-webkit-scrollbar-thumb { background: var(--bg-3); border-radius: 99px; }

    /* ── Header ───────────────────────────────────────────────────── */
    .app-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.6rem 0 1.2rem;
        border-bottom: 1px solid var(--border);
        margin-bottom: 2.5rem;
    }
    .app-logo {
        font-family: var(--font-display);
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--text-1);
    }
    .app-logo span { color: var(--gold); }
    .app-badge {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: var(--text-3);
        background: var(--bg-3);
        border: 1px solid var(--border);
        padding: 0.3rem 0.8rem;
        border-radius: 99px;
    }

    /* ── Hero Card ────────────────────────────────────────────────── */
    .hero-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, #0d1729 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 3.5rem 3rem;
        text-align: center;
        box-shadow: var(--shadow-card), 0 0 80px rgba(79,163,255,0.05);
        position: relative;
        overflow: hidden;
        margin: 1rem 0 2rem;
    }
    .hero-card::before {
        content: '';
        position: absolute;
        top: -60px; right: -60px;
        width: 240px; height: 240px;
        background: radial-gradient(circle, rgba(240,180,41,0.08) 0%, transparent 70%);
        border-radius: 50%;
        pointer-events: none;
    }
    .hero-icon {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        filter: drop-shadow(0 0 20px rgba(240,180,41,0.4));
    }
    .hero-title {
        font-family: var(--font-display);
        font-size: 2.1rem;
        font-weight: 800;
        line-height: 1.18;
        letter-spacing: -0.03em;
        color: var(--text-1);
        margin-bottom: 1rem;
    }
    .hero-subtitle {
        font-size: 1.05rem;
        font-weight: 300;
        color: var(--text-2);
        line-height: 1.7;
        margin-bottom: 2rem;
    }
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.7rem;
        margin-top: 1.5rem;
    }
    .feature-item {
        background: var(--bg-3);
        border: 1px solid var(--border);
        border-radius: var(--radius-sm);
        padding: 0.6rem 0.8rem;
        font-size: 0.83rem;
        font-weight: 500;
        color: var(--text-2);
    }

    /* ── Buttons ──────────────────────────────────────────────────── */
    .stButton > button {
        font-family: var(--font-display) !important;
        font-weight: 700 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.02em !important;
        border-radius: var(--radius-md) !important;
        border: 1px solid rgba(79,163,255,0.4) !important;
        background: linear-gradient(135deg, #1a3a6a 0%, #0f2247 100%) !important;
        color: var(--blue) !important;
        padding: 0.7rem 1.5rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 12px rgba(79,163,255,0.15) !important;
    }
    .stButton > button:hover {
        border-color: var(--blue) !important;
        box-shadow: 0 4px 20px rgba(79,163,255,0.3) !important;
        transform: translateY(-1px) !important;
    }
    [data-testid="baseButton-primary"] > button,
    button[kind="primary"] {
        background: linear-gradient(135deg, var(--gold) 0%, var(--gold-dim) 100%) !important;
        color: #050810 !important;
        border-color: var(--gold) !important;
        box-shadow: 0 4px 20px rgba(240,180,41,0.3) !important;
    }

    /* ── Metric Cards ─────────────────────────────────────────────── */
    .metric-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.3rem 1.5rem;
        box-shadow: var(--shadow-card);
        transition: border-color 0.2s;
        height: 100%;
    }
    .metric-card:hover { border-color: var(--border-glow); }
    .metric-label {
        font-size: 0.78rem;
        font-weight: 500;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-3);
        margin-bottom: 0.6rem;
    }
    .metric-value {
        font-family: var(--font-numbers);
        font-size: 2rem;
        font-weight: 400;
        letter-spacing: 0.01em;
        line-height: 1;
    }

    /* ── Section Title ────────────────────────────────────────────── */
    .section-title {
        font-family: var(--font-display);
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: 0.02em;
        color: var(--text-1);
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid var(--border);
    }

    /* ── Results Header ───────────────────────────────────────────── */
    .results-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    .profile-badge {
        display: inline-block;
        border: 2px solid;
        border-radius: 99px;
        padding: 0.4rem 1.4rem;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }
    .results-title {
        font-family: var(--font-display);
        font-size: 1.8rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.3rem;
    }
    .results-sub { color: var(--text-2); font-size: 0.9rem; }

    /* ── AI Response ──────────────────────────────────────────────── */
    .ai-response {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 3px solid var(--blue);
        border-radius: var(--radius-md);
        padding: 1.5rem;
        line-height: 1.75;
        color: var(--text-2);
        font-size: 0.93rem;
        white-space: pre-wrap;
    }
    .ai-placeholder {
        background: var(--bg-card);
        border: 1px dashed var(--border);
        border-radius: var(--radius-md);
        padding: 3rem 2rem;
        text-align: center;
        color: var(--text-3);
    }
    .ai-placeholder-icon { font-size: 2.5rem; margin-bottom: 0.8rem; }

    /* ── Alert Cards ──────────────────────────────────────────────── */
    .alert-card {
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
        margin-bottom: 0.8rem;
        font-size: 0.88rem;
    }
    .alert-high   { border-left: 3px solid var(--red); }
    .alert-medium { border-left: 3px solid var(--gold); }
    .alert-low    { border-left: 3px solid var(--green); }
    .alert-icon   { font-size: 1.2rem; margin-top: 0.1rem; flex-shrink: 0; }

    /* ── Form Elements ────────────────────────────────────────────── */
    .stSlider > div > div { background: var(--bg-3) !important; }
    .stSlider [data-baseweb="slider"] [data-testid="stThumbValue"] {
        background: var(--blue) !important;
    }
    .stRadio > label { font-size: 0.9rem !important; color: var(--text-2) !important; }
    .stSelectbox > div > div {
        background: var(--bg-2) !important;
        border-color: var(--border) !important;
        border-radius: var(--radius-sm) !important;
        color: var(--text-1) !important;
    }
    .stNumberInput > div > div > input {
        background: var(--bg-2) !important;
        border-color: var(--border) !important;
        color: var(--text-1) !important;
    }

    /* ── Progress Step ────────────────────────────────────────────── */
    .step-progress {
        display: flex;
        justify-content: center;
        gap: 0.5rem;
        margin-bottom: 2rem;
    }
    .step-dot {
        width: 8px; height: 8px;
        border-radius: 50%;
        background: var(--bg-3);
        border: 1px solid var(--border);
        transition: all 0.3s;
    }
    .step-dot.active {
        background: var(--gold);
        border-color: var(--gold);
        width: 24px; border-radius: 4px;
    }
    .step-dot.done { background: var(--green); border-color: var(--green); }

    /* ── Native table (column-based) ─────────────────────────────── */
    .tbl-header {
        font-family: var(--font-display);
        font-size: 0.7rem;
        font-weight: 700;
        letter-spacing: 0.09em;
        text-transform: uppercase;
        color: var(--text-3);
        padding: 0.5rem 0.3rem 0.6rem;
    }
    .tbl-divider {
        border-top: 1px solid var(--border);
        margin: 0 0 0.15rem;
    }
    .tbl-cell {
        font-size: 0.87rem;
        color: var(--text-2);
        padding: 0.55rem 0.3rem;
        border-bottom: 1px solid rgba(99,120,180,0.08);
        min-height: 52px;
    }
    .tbl-text { color: var(--text-2); font-size: 0.82rem; }
    .asset-name { color: #eef2ff; font-weight: 600; font-size: 0.88rem; }
    .asset-sub  { color: var(--text-3); font-size: 0.73rem; }
    .asset-dot {
        display: inline-block;
        width: 10px; height: 10px;
        border-radius: 50%;
        margin-right: 8px;
        vertical-align: middle;
    }
    .pct-bar-bg {
        background: var(--bg-3);
        border-radius: 99px;
        height: 6px;
        width: 100%;
        overflow: hidden;
    }
    .pct-bar-fill {
        height: 100%;
        border-radius: 99px;
        transition: width 0.8s ease;
    }
    .tag {
        display: inline-block;
        font-size: 0.7rem;
        font-weight: 600;
        letter-spacing: 0.06em;
        padding: 0.2rem 0.6rem;
        border-radius: 4px;
        text-transform: uppercase;
    }

    /* ── Tabs ─────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-1) !important;
        border-radius: var(--radius-sm) !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid var(--border) !important;
    }
    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-3) !important;
        border-radius: 6px !important;
        font-family: var(--font-body) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    .stTabs [aria-selected="true"] {
        background: var(--bg-3) !important;
        color: var(--text-1) !important;
    }
    .stTabs [data-baseweb="tab-highlight"] { display: none !important; }

    /* ── Expander ─────────────────────────────────────────────────── */
    .streamlit-expanderHeader {
        background: var(--bg-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        font-size: 0.85rem !important;
        color: var(--text-2) !important;
    }
    .streamlit-expanderContent {
        background: var(--bg-1) !important;
        border: 1px solid var(--border) !important;
        border-top: none !important;
    }

    /* ── Footer ───────────────────────────────────────────────────── */
    .app-footer {
        margin-top: 4rem;
        padding: 1.5rem 0;
        border-top: 1px solid var(--border);
        text-align: center;
        font-size: 0.78rem;
        color: var(--text-3);
    }
    .disclaimer {
        font-size: 0.75rem;
        color: var(--text-3);
        margin-top: 1.5rem;
        padding: 0.8rem;
        background: rgba(240,180,41,0.05);
        border: 1px solid rgba(240,180,41,0.15);
        border-radius: var(--radius-sm);
    }

    /* ── Audience note (intro) ────────────────────────────────── */
    .audience-note {
        background: rgba(79,163,255,0.07);
        border: 1px solid rgba(79,163,255,0.2);
        border-radius: var(--radius-md);
        padding: 1rem 1.4rem;
        font-size: 0.9rem;
        color: var(--text-2);
        text-align: center;
    }

    /* ── Profiler card ────────────────────────────────────────── */
    .profiler-card {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 2.2rem 2rem 1.5rem;
        box-shadow: var(--shadow-card);
        margin-bottom: 1.5rem;
    }
    .q-emoji { font-size: 2.2rem; margin-bottom: 0.6rem; }
    .q-title {
        font-family: var(--font-display);
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: var(--text-1);
    }
    .profiler-card p.hint {
        font-size: 0.84rem;
        color: var(--text-3);
        margin-bottom: 0;
    }

    /* ── Summary panel ────────────────────────────────────────── */
    .summary-panel {
        background: linear-gradient(135deg, var(--bg-card) 0%, #0d1e35 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 2rem 2.2rem;
        box-shadow: var(--shadow-card);
        margin-bottom: 1.5rem;
    }
    .summary-top { text-align: center; margin-bottom: 1.8rem; }
    .profile-pill {
        display: inline-block;
        border-radius: 99px;
        padding: 0.35rem 1.2rem;
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-bottom: 0.9rem;
    }
    .summary-title {
        font-family: var(--font-display);
        font-size: 1.6rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        margin-bottom: 0.5rem;
        color: var(--text-1);
    }
    .summary-explain {
        color: var(--text-2);
        font-size: 0.95rem;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.65;
    }
    .summary-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    .summary-item {
        background: var(--bg-3);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem;
        text-align: center;
    }
    .si-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: var(--text-3);
        margin-bottom: 0.4rem;
    }
    .si-value {
        font-family: var(--font-display);
        font-size: 1.3rem;
        font-weight: 800;
        color: var(--text-1);
    }
    .summary-desc {
        background: rgba(79,163,255,0.06);
        border: 1px solid rgba(79,163,255,0.15);
        border-left: 3px solid var(--blue);
        border-radius: var(--radius-md);
        padding: 1rem 1.4rem;
        font-size: 0.91rem;
        color: var(--text-2);
        line-height: 1.7;
    }

    /* ── Metric card sub ──────────────────────────────────────── */
    .metric-sub {
        font-size: 0.72rem;
        color: var(--text-3);
        margin-top: 0.3rem;
    }

    /* ── Remove asset button (✕) ─────────────────────────────── */
    button:has(> div > p:only-child) {
        padding: 0.25rem 0.55rem !important;
        font-size: 0.8rem !important;
        border-radius: 6px !important;
        border-color: rgba(239,68,68,0.3) !important;
        color: #f87171 !important;
        background: rgba(239,68,68,0.08) !important;
        box-shadow: none !important;
    }

    /* ── Radio options styled ─────────────────────────────────── */
    .stRadio [data-baseweb="radio"] {
        background: var(--bg-2) !important;
        border: 1px solid var(--border) !important;
        border-radius: var(--radius-sm) !important;
        padding: 0.7rem 1rem !important;
        margin-bottom: 0.4rem !important;
        transition: border-color 0.2s !important;
    }
    .stRadio [data-baseweb="radio"]:hover {
        border-color: var(--blue) !important;
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="app-header">
        <div class="app-logo">Finanzas<span>IA</span></div>
        <div class="app-badge">⚡ Powered by Claude AI</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="app-footer">
        FinanzasIA · Solo para fines educativos · No constituye asesoramiento financiero profesional<br>
        Construido con Streamlit + Claude AI · Argentina 🇦🇷
    </div>
    """, unsafe_allow_html=True)
