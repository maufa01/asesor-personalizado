"""
Configuración visual y CSS personalizado para FinanzasIA
Aesthetic: Luxury Dark Finance — inspired by Bloomberg terminals and premium trading platforms
"""

import streamlit as st


def apply_custom_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&family=Space+Grotesk:wght@300;400;500;600;700&display=swap');

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
        --font-numbers: 'Space Grotesk', sans-serif;
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
    
    /* ── Responsive Container ─────────────────────────────────────── */
    @media (max-width: 1024px) {
        .block-container {
            padding: 0 1.5rem 3rem !important;
            max-width: 100% !important;
        }
    }
    
    @media (max-width: 640px) {
        .block-container {
            padding: 0 1rem 2rem !important;
        }
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
        flex-wrap: wrap;
        gap: 1rem;
    }
    
    @media (max-width: 640px) {
        .app-header {
            padding: 1rem 0 0.8rem;
            margin-bottom: 1.5rem;
            justify-content: center;
            text-align: center;
        }
    }
    
    .app-logo {
        font-family: var(--font-display);
        font-size: 1.5rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: var(--text-1);
    }
    
    @media (max-width: 640px) {
        .app-logo {
            font-size: 1.2rem;
        }
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
    
    @media (max-width: 640px) {
        .app-badge {
            font-size: 0.65rem;
            padding: 0.25rem 0.6rem;
        }
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
    
    @media (max-width: 768px) {
        .hero-card {
            padding: 2.5rem 2rem;
            margin: 0.5rem 0 1.5rem;
        }
    }
    
    @media (max-width: 640px) {
        .hero-card {
            padding: 1.8rem 1.5rem;
            margin: 0.5rem 0 1rem;
        }
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
    .hero-features {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 0.9rem;
        margin-top: 2rem;
    }
    @media (max-width: 768px) {
        .hero-features { grid-template-columns: repeat(2, 1fr); gap: 0.7rem; }
    }
    @media (max-width: 480px) {
        .hero-features { grid-template-columns: 1fr 1fr; gap: 0.5rem; margin-top: 1.2rem; }
    }
    .hero-feature-pill {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        padding: 1rem 1.1rem;
        border-radius: var(--radius-md);
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.07);
        color: var(--text-2);
        font-weight: 600;
        transition: transform 0.2s ease, border-color 0.2s ease, color 0.2s ease;
    }
    .hero-feature-pill:hover {
        transform: translateY(-1px);
        border-color: rgba(79,163,255,0.3);
        color: var(--text-1);
    }
    @media (max-width: 768px) {
        .hero-feature-pill { padding: 0.8rem 0.9rem; font-size: 0.88rem; gap: 0.55rem; }
    }
    @media (max-width: 480px) {
        .hero-feature-pill { padding: 0.65rem 0.7rem; font-size: 0.78rem; gap: 0.4rem; }
    }
    .hero-feature-icon {
        font-size: 1.2rem;
    }
    @media (max-width: 480px) {
        .hero-feature-icon { font-size: 1rem; }
    }
    
    @media (max-width: 640px) {
        .hero-icon {
            font-size: 2.5rem;
            margin-bottom: 0.8rem;
        }
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
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.6rem;
        }
    }
    
    @media (max-width: 640px) {
        .hero-title {
            font-size: 1.3rem;
            margin-bottom: 0.8rem;
        }
    }
    
    .hero-subtitle {
        font-size: 1.05rem;
        font-weight: 300;
        color: var(--text-2);
        line-height: 1.7;
        margin-bottom: 2rem;
    }
    
    @media (max-width: 768px) {
        .hero-subtitle {
            font-size: 0.95rem;
            margin-bottom: 1.5rem;
        }
    }
    
    @media (max-width: 640px) {
        .hero-subtitle {
            font-size: 0.85rem;
            margin-bottom: 1rem;
            line-height: 1.5;
        }
    }
    
    .hero-human-copy {
        font-size: 1rem;
        font-weight: 400;
        color: var(--text-2);
        margin-top: 1.2rem;
        opacity: 0.85;
        font-style: italic;
    }

    @media (max-width: 640px) {
        .hero-human-copy {
            font-size: 0.9rem;
        }
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
        width: 100% !important;
    }
    
    @media (max-width: 640px) {
        .stButton > button {
            font-size: 0.8rem !important;
            padding: 0.6rem 1.2rem !important;
        }
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
    
    @media (max-width: 1024px) {
        .metric-card {
            padding: 1rem 1.2rem;
        }
    }
    
    @media (max-width: 640px) {
        .metric-card {
            padding: 0.8rem 1rem;
        }
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
    
    @media (max-width: 640px) {
        .metric-label {
            font-size: 0.65rem;
            margin-bottom: 0.4rem;
        }
    }
    
    .metric-value {
        font-family: var(--font-numbers);
        font-size: 2rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        line-height: 1;
        font-variant-numeric: tabular-nums;
    }
    
    @media (max-width: 768px) {
        .metric-value {
            font-size: 1.5rem;
        }
    }
    
    @media (max-width: 640px) {
        .metric-value {
            font-size: 1.2rem;
        }
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
    
    @media (max-width: 768px) {
        .section-title {
            font-size: 0.95rem;
            margin-bottom: 0.8rem;
        }
    }
    
    @media (max-width: 640px) {
        .section-title {
            font-size: 0.85rem;
            margin-bottom: 0.6rem;
        }
    }

    .chart-headline {
        font-family: var(--font-display);
        font-size: 1.05rem;
        font-weight: 600;
        color: var(--green);
        margin: 0 0 0.75rem 0;
        line-height: 1.4;
    }
    @media (max-width: 768px) {
        .chart-headline { font-size: 0.95rem; }
    }
    .chart-currency-note {
        font-size: 0.72rem;
        color: var(--text-3);
        text-align: center;
        margin: -0.25rem 0 0.75rem 0;
        font-style: italic;
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
    @media (max-width: 768px) { .results-title { font-size: 1.4rem; } }
    @media (max-width: 480px) { .results-title { font-size: 1.15rem; } }
    .results-sub { color: var(--text-2); font-size: 0.9rem; }

    /* ── AI Response ──────────────────────────────────────────────── */
    .ai-response {
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-left: 3px solid var(--blue);
        border-radius: var(--radius-md);
        padding: 1.5rem 1.75rem;
        line-height: 1.8;
        color: var(--text-2);
        font-size: 1rem;
    }
    .ai-response p { margin: 0 0 0.9rem 0; }
    .ai-section { margin-bottom: 1.6rem; }
    .ai-section-title {
        font-size: 0.95rem;
        font-weight: 700;
        color: var(--text-1);
        margin: 0 0 1rem 0;
        padding-bottom: 0.45rem;
        border-bottom: 1px solid var(--border);
        letter-spacing: 0.01em;
    }
    .asset-card {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-left: 3px solid var(--blue);
        border-radius: 8px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.85rem;
    }
    .asset-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.6rem;
    }
    .asset-name {
        font-weight: 700;
        font-size: 0.97rem;
        color: var(--text-1);
    }
    .asset-weight {
        background: var(--blue);
        color: #fff;
        font-size: 0.78rem;
        font-weight: 700;
        padding: 2px 10px;
        border-radius: 20px;
        letter-spacing: 0.03em;
    }
    .asset-row {
        font-size: 0.94rem;
        margin-bottom: 0.4rem;
        color: var(--text-2);
    }
    .asset-row strong { color: var(--text-1); margin-right: 4px; }
    .asset-row-risk { color: rgba(248,113,113,0.85) !important; }
    .asset-row-risk strong { color: #f87171 !important; }
    .ai-intro {
        background: rgba(96,165,250,0.07);
        border: 1px solid rgba(96,165,250,0.2);
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 1.4rem;
        font-size: 0.91rem;
        color: var(--text-2);
        line-height: 1.7;
    }
    .ai-tip-list { list-style: none; padding: 0; margin: 0; }
    .ai-tip-list li {
        padding: 0.55rem 0;
        border-bottom: 1px solid var(--border);
        font-size: 0.9rem;
        color: var(--text-2);
        display: flex;
        gap: 0.6rem;
        align-items: flex-start;
    }
    .ai-tip-list li:last-child { border-bottom: none; }
    .ai-tip-list li span.tip-icon { font-size: 1rem; flex-shrink: 0; padding-top: 1px; }
    .rebalance-block {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-bottom: 0.85rem;
    }
    .rebalance-block strong { color: var(--text-1); display: block; margin-bottom: 0.3rem; font-size: 0.9rem; }

    /* ── Chat ─────────────────────────────────────────────────────────── */
    .chat-bubble {
        max-width: 82%;
        margin-bottom: 0.75rem;
        padding: 0.75rem 1rem;
        border-radius: 12px;
        font-size: 0.9rem;
        line-height: 1.65;
    }
    @media (max-width: 640px) {
        .chat-bubble { max-width: 96%; font-size: 0.85rem; padding: 0.65rem 0.85rem; }
    }
    .chat-label {
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.04em;
        margin-bottom: 0.3rem;
        opacity: 0.6;
        text-transform: uppercase;
    }
    .chat-text { color: var(--text-1); white-space: pre-wrap; font-size: 0.97rem; line-height: 1.7; }
    .chat-user {
        background: rgba(96,165,250,0.1);
        border: 1px solid rgba(96,165,250,0.25);
        margin-left: auto;
        text-align: right;
    }
    .chat-advisor {
        background: rgba(255,255,255,0.04);
        border: 1px solid var(--border);
        margin-right: auto;
    }
    /* ── AI Empty State ───────────────────────────────────────────── */
    @keyframes aiIconPulse {
        0%, 100% { transform: scale(1);    filter: drop-shadow(0 0 10px rgba(79,163,255,0.4)); }
        50%       { transform: scale(1.1);  filter: drop-shadow(0 0 22px rgba(79,163,255,0.75)); }
    }
    @keyframes aiBtnGlow {
        0%, 100% { box-shadow: 0 2px 12px rgba(79,163,255,0.15) !important; }
        50%       { box-shadow: 0 2px 28px rgba(79,163,255,0.55), 0 0 48px rgba(79,163,255,0.2) !important; }
    }
    .ai-empty-state {
        background: linear-gradient(135deg, var(--bg-card) 0%, #0a1628 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 2.5rem 2rem 2rem;
        text-align: center;
        margin-bottom: 1.2rem;
    }
    .ai-empty-icon {
        font-size: 3rem;
        display: inline-block;
        margin-bottom: 1rem;
        animation: aiIconPulse 2.5s ease-in-out infinite;
    }
    .ai-empty-title {
        font-family: var(--font-display);
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-1);
        margin-bottom: 1.2rem;
    }
    .ai-empty-bullets {
        display: inline-flex;
        flex-direction: column;
        gap: 0.5rem;
        text-align: left;
        margin: 0 auto;
    }
    .ai-bullet {
        font-size: 0.88rem;
        color: var(--text-2);
        padding: 0.35rem 0.8rem;
        background: rgba(79,163,255,0.06);
        border-left: 2px solid var(--blue);
        border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    }
    /* Glow on the CTA button that follows the marker div */
    div[data-testid="stMarkdownContainer"]:has(.ai-cta-marker) + div[data-testid="stHorizontalBlock"] button,
    div[data-testid="stMarkdownContainer"]:has(.ai-cta-marker) ~ div[data-testid="stHorizontalBlock"] button {
        animation: aiBtnGlow 2s ease-in-out infinite !important;
        border-color: var(--blue) !important;
    }

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
    .stRadio > label { font-size: 1rem !important; color: var(--text-2) !important; }
    div[data-testid="stRadio"] div[role="radiogroup"] label,
    div[data-testid="stRadio"] div[role="radiogroup"] label p {
        color: #d0d5e0 !important;
        font-size: 1rem !important;
    }
    @media (max-width: 640px) {
        div[data-testid="stRadio"] div[role="radiogroup"] label,
        div[data-testid="stRadio"] div[role="radiogroup"] label p {
            font-size: 1rem !important;
        }
    }
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
        font-size: 0.75rem;
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
        font-size: 0.93rem;
        color: var(--text-2);
        padding: 0.65rem 0.3rem;
        border-bottom: 1px solid rgba(99,120,180,0.08);
        min-height: 56px;
    }
    .tbl-text { color: var(--text-2); font-size: 0.9rem; }
    .asset-name { color: #eef2ff; font-weight: 600; font-size: 0.95rem; }
    .asset-sub  { color: var(--text-3); font-size: 0.8rem; }
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

    /* ── Asset Simple View ────────────────────────────────────────── */
    .asset-simple-card {
        display: flex;
        align-items: center;
        gap: 1rem;
        background: var(--bg-3);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem 1.2rem;
        margin-bottom: 0.6rem;
        transition: border-color 0.2s;
    }
    .asset-simple-card:hover { border-color: rgba(79,163,255,0.3); }
    .asc-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        flex-shrink: 0;
    }
    .asc-content { flex: 1; min-width: 0; }
    .asc-name {
        font-weight: 600;
        color: var(--text-1);
        font-size: 0.9rem;
        margin-bottom: 0.2rem;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
    .asc-desc {
        font-size: 0.78rem;
        color: var(--text-2);
        line-height: 1.4;
    }
    .asc-pct {
        font-family: var(--font-numbers);
        font-size: 1.3rem;
        font-weight: 700;
        color: var(--text-1);
        text-align: right;
        flex-shrink: 0;
        line-height: 1.1;
    }
    .asc-pct-sub {
        display: block;
        font-size: 0.6rem;
        font-weight: 400;
        color: var(--text-3);
        font-family: var(--font-body);
    }
    @media (max-width: 640px) {
        .asc-name { font-size: 0.82rem; }
        .asc-desc { font-size: 0.72rem; }
        .asc-pct  { font-size: 1.1rem; }
    }

    /* ── Floating Action Button ───────────────────────────────────── */
    @keyframes fabSlideUp {
        from { opacity: 0; transform: translateY(20px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .fab-btn {
        position: fixed;
        bottom: calc(2rem + env(safe-area-inset-bottom));
        right: calc(2rem + env(safe-area-inset-right));
        z-index: 9999;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dim) 100%);
        color: #fff !important;
        padding: 0.85rem 1.4rem;
        border-radius: 99px;
        font-family: var(--font-display);
        font-weight: 700;
        font-size: 0.88rem;
        text-decoration: none !important;
        box-shadow: 0 4px 24px rgba(79,163,255,0.45);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        animation: fabSlideUp 0.45s ease-out 1.5s both;
        white-space: nowrap;
        -webkit-tap-highlight-color: transparent;
        min-height: 44px; /* touch target iOS */
    }
    .fab-btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 32px rgba(79,163,255,0.6);
    }
    @media (max-width: 640px) {
        .fab-btn {
            bottom: calc(1.2rem + env(safe-area-inset-bottom));
            right: calc(1rem + env(safe-area-inset-right));
            font-size: 0.8rem;
            padding: 0.7rem 1.1rem;
        }
    }

    /* ── Remove Confirm Banner ────────────────────────────────────── */
    .remove-confirm {
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.3);
        border-radius: var(--radius-sm);
        padding: 0.75rem 1rem;
        font-size: 0.88rem;
        color: var(--text-2);
        margin-bottom: 0.75rem;
        line-height: 1.5;
    }
    .remove-confirm strong { color: var(--text-1); }

    /* ── Tabs ─────────────────────────────────────────────────────── */
    .stTabs [data-baseweb="tab-list"] {
        background: var(--bg-1) !important;
        border-radius: var(--radius-sm) !important;
        padding: 4px !important;
        gap: 4px !important;
        border: 1px solid var(--border) !important;
    }
    
    @media (max-width: 640px) {
        .stTabs [data-baseweb="tab-list"] {
            padding: 2px !important;
            gap: 2px !important;
            overflow-x: auto !important;
            flex-wrap: nowrap !important;
            -webkit-overflow-scrolling: touch;
        }
    }

    .stTabs [data-baseweb="tab"] {
        background: transparent !important;
        color: var(--text-3) !important;
        border-radius: 6px !important;
        font-family: var(--font-body) !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
    }
    
    @media (max-width: 640px) {
        .stTabs [data-baseweb="tab"] {
            font-size: 0.7rem !important;
            padding: 0.3rem 0.5rem !important;
        }
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
    
    @media (max-width: 768px) {
        .profiler-card {
            padding: 1.5rem 1.5rem 1.2rem;
            margin-bottom: 1rem;
        }
    }
    
    @media (max-width: 640px) {
        .profiler-card {
            padding: 1.2rem 1rem 1rem;
            margin-bottom: 0.8rem;
        }
    }
    
    .q-emoji { 
        font-size: 2.2rem;
        margin-bottom: 0.6rem;
    }
    
    @media (max-width: 640px) {
        .q-emoji {
            font-size: 1.8rem;
            margin-bottom: 0.5rem;
        }
    }
    
    .q-title {
        font-family: var(--font-display);
        font-size: 1.25rem;
        font-weight: 700;
        margin-bottom: 0.4rem;
        color: var(--text-1);
    }
    
    @media (max-width: 768px) {
        .q-title {
            font-size: 1.1rem;
        }
    }
    
    @media (max-width: 640px) {
        .q-title {
            font-size: 0.95rem;
        }
    }
    
    .profiler-card p.hint {
        font-size: 0.84rem;
        color: var(--text-3);
        margin-bottom: 0;
    }

    @media (max-width: 640px) {
        .profiler-card p.hint {
            font-size: 0.75rem;
        }
    }

    .progress-wrap {
        margin-bottom: 1.2rem;
    }
    .progress-label {
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: var(--text-2);
        margin-bottom: 0.4rem;
        opacity: 0.7;
    }
    .progress-track {
        width: 100%;
        height: 6px;
        background: var(--bg-3);
        border-radius: 99px;
        overflow: hidden;
    }
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--blue-dim), var(--blue));
        border-radius: 99px;
        transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ── Profile Reveal ───────────────────────────────────────── */
    .reveal-card {
        background: linear-gradient(135deg, var(--bg-card) 0%, #0a1628 100%);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 2.5rem 2.2rem 2rem;
        text-align: center;
        box-shadow: var(--shadow-card);
        margin-bottom: 1.5rem;
    }
    @media (max-width: 768px) { .reveal-card { padding: 1.8rem 1.5rem 1.5rem; } }
    @media (max-width: 480px) { .reveal-card { padding: 1.2rem 1rem; margin-bottom: 1rem; } }
    .reveal-badge {
        display: inline-block;
        font-family: var(--font-display);
        font-size: 1.4rem;
        font-weight: 800;
        border: 2px solid;
        border-radius: 99px;
        padding: 0.5rem 1.6rem;
        margin-bottom: 1rem;
        letter-spacing: -0.01em;
    }
    @media (max-width: 480px) { .reveal-badge { font-size: 1.1rem; padding: 0.4rem 1.1rem; } }
    .reveal-tagline {
        font-size: 1.1rem;
        font-weight: 600;
        color: var(--text-1);
        margin-bottom: 0.8rem;
    }
    @media (max-width: 480px) { .reveal-tagline { font-size: 0.95rem; } }
    .reveal-explanation {
        font-size: 0.93rem;
        color: var(--text-2);
        line-height: 1.75;
        max-width: 600px;
        margin: 0 auto;
    }
    @media (max-width: 480px) { .reveal-explanation { font-size: 0.82rem; line-height: 1.6; } }
    .reveal-columns {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    @media (max-width: 768px) {
        .reveal-columns {
            grid-template-columns: 1fr;
        }
    }
    .reveal-section {
        background: rgba(255,255,255,0.03);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1.2rem 1.4rem;
        text-align: left;
    }
    .reveal-section-title {
        font-size: 0.82rem;
        font-weight: 700;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        color: var(--text-3);
        margin-bottom: 0.85rem;
    }
    .reveal-item {
        font-size: 0.88rem;
        color: var(--text-2);
        padding: 0.4rem 0;
        border-bottom: 1px solid rgba(99,120,180,0.1);
        line-height: 1.5;
    }
    .reveal-item:last-child { border-bottom: none; }

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
    @media (max-width: 768px) { .summary-title { font-size: 1.25rem; } }
    @media (max-width: 480px) { .summary-title { font-size: 1.05rem; } }
    .summary-explain {
        color: var(--text-2);
        font-size: 1.05rem;
        max-width: 600px;
        margin: 0 auto;
        line-height: 1.7;
        text-align: center;
    }
    
    @media (max-width: 768px) {
        .summary-explain {
            font-size: 0.88rem;
        }
    }
    
    @media (max-width: 640px) {
        .summary-explain {
            font-size: 0.8rem;
        }
    }
    
    .summary-grid {
        display: grid;
        gap: 1rem;
        margin-bottom: 1rem;
    }
    .summary-main-grid {
        grid-template-columns: repeat(3, 1fr);
    }
    .summary-detail-grid {
        grid-template-columns: repeat(3, 1fr);
        margin-top: 0.75rem;
    }

    @media (max-width: 768px) {
        .summary-main-grid,
        .summary-detail-grid {
            grid-template-columns: repeat(2, 1fr);
            gap: 0.6rem;
        }
    }

    @media (max-width: 480px) {
        .summary-main-grid,
        .summary-detail-grid {
            grid-template-columns: 1fr;
            gap: 0.5rem;
        }
    }

    .summary-detail {
        margin-bottom: 1rem;
    }
    .summary-detail-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.4rem;
        list-style: none;
        cursor: pointer;
        font-size: 0.78rem;
        font-weight: 600;
        color: var(--blue);
        padding: 0.5rem 1rem;
        border: 1px solid rgba(79,163,255,0.25);
        border-radius: var(--radius-sm);
        background: rgba(79,163,255,0.05);
        transition: background 0.2s, border-color 0.2s;
        user-select: none;
        width: 100%;
        box-sizing: border-box;
    }
    .summary-detail-btn::-webkit-details-marker { display: none; }
    .summary-detail-btn::marker { display: none; }
    .summary-detail-btn::after {
        content: "↓";
        display: inline-block;
        transition: transform 0.3s ease;
    }
    .summary-detail[open] .summary-detail-btn::after {
        transform: rotate(180deg);
    }
    .summary-detail-btn:hover {
        background: rgba(79,163,255,0.1);
        border-color: rgba(79,163,255,0.45);
    }

    @keyframes detailSlideDown {
        from { opacity: 0; transform: translateY(-6px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .summary-detail[open] .summary-detail-grid {
        animation: detailSlideDown 0.25s ease-out;
    }
    
    .summary-item {
        background: var(--bg-3);
        border: 1px solid var(--border);
        border-radius: var(--radius-md);
        padding: 1rem;
        text-align: center;
    }
    
    @media (max-width: 640px) {
        .summary-item {
            padding: 0.8rem;
        }
    }
    
    .si-label {
        font-size: 0.72rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.07em;
        color: var(--text-3);
        margin-bottom: 0.4rem;
    }
    
    @media (max-width: 640px) {
        .si-label {
            font-size: 0.65rem;
        }
    }
    
    .si-value {
        font-family: var(--font-numbers);
        font-size: 1.3rem;
        font-weight: 600;
        letter-spacing: -0.02em;
        font-variant-numeric: tabular-nums;
        color: var(--text-1);
    }
    .si-sub {
        font-size: 0.65rem;
        color: var(--text-3);
        margin-top: 0.25rem;
        line-height: 1.3;
    }
    .summary-desc {
        background: rgba(79,163,255,0.06);
        border: 1px solid rgba(79,163,255,0.15);
        border-left: 3px solid var(--blue);
        border-radius: var(--radius-md);
        padding: 1rem 1.4rem;
        font-size: 1rem;
        color: var(--text-2);
        line-height: 1.75;
        text-align: center;
    }

    .action-guide {
        display: grid;
        gap: 1rem;
        margin-top: 1rem;
        background: var(--bg-card);
        border: 1px solid var(--border);
        border-radius: var(--radius-lg);
        padding: 1.5rem 1.6rem;
    }
    .action-step {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 1rem;
        align-items: start;
        padding: 1rem 0;
        border-bottom: 1px solid rgba(255,255,255,0.06);
    }
    .action-step:last-child { border-bottom: none; }
    .action-step-number {
        width: 2.7rem;
        height: 2.7rem;
        min-width: 2.7rem;
        border-radius: 50%;
        display: grid;
        place-items: center;
        font-weight: 700;
        color: var(--bg-0);
        background: var(--gold);
        font-size: 1rem;
    }
    .action-step-body {
        display: grid;
        gap: 0.3rem;
    }
    .action-step-title {
        font-family: var(--font-display);
        font-size: 1rem;
        font-weight: 700;
        color: var(--text-1);
    }
    .action-step-copy {
        color: var(--text-2);
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .action-step-help {
        margin-top: 0.55rem;
        border: 1px solid rgba(79,163,255,0.15);
        border-radius: var(--radius-sm);
        background: rgba(79,163,255,0.04);
        padding: 0.75rem 1rem;
    }
    .action-step-help summary {
        cursor: pointer;
        font-weight: 600;
        color: var(--blue);
        list-style: none;
    }
    .action-step-help summary::-webkit-details-marker { display: none; }
    .action-step-help div {
        margin-top: 0.7rem;
        color: var(--text-2);
        font-size: 0.9rem;
        line-height: 1.6;
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

    /* ── Responsive Columns: stack on tablet & mobile ────────────── */
    @media (max-width: 768px) {
        [data-testid="stHorizontalBlock"] {
            flex-direction: column !important;
            gap: 0.75rem !important;
        }
        [data-testid="stHorizontalBlock"] > [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            flex: unset !important;
        }
    }

    /* ── Metrics grid (4 KPIs responsive) ─────────────────────────── */
    .metrics-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
        margin-bottom: 1rem;
    }
    @media (max-width: 1024px) {
        .metrics-grid { grid-template-columns: repeat(2, 1fr); gap: 0.75rem; }
    }
    @media (max-width: 480px) {
        .metrics-grid { grid-template-columns: 1fr 1fr; gap: 0.5rem; }
    }
    @media (max-width: 360px) {
        .metrics-grid { grid-template-columns: 1fr; }
    }

    /* ── Make Streamlit containers responsive ───────────────────── */
    @media (max-width: 640px) {
        [data-testid="stMetricContainer"] {
            margin-bottom: 0.5rem !important;
        }
    }

    /* ── Mobile form elements ──────────────────────────────────────– */
    @media (max-width: 640px) {
        input, textarea, select, [data-baseweb="select"] {
            font-size: 16px !important; /* evita zoom automático en iOS */
        }
        .stSlider > div {
            padding: 0.5rem 0 !important;
        }
    }

    /* ── Ensure text doesn't overflow ──────────────────────────────– */
    @media (max-width: 640px) {
        p, span, div {
            word-break: break-word !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown("""
    <div class="app-header">
        <div class="app-logo">Finanzas<span>IA</span></div>
        <div class="app-badge">Asesoramiento Financiero Digital</div>
    </div>
    """, unsafe_allow_html=True)


def render_footer():
    st.markdown("""
    <div class="app-footer">
        FinanzasIA · Herramienta educativa de planificación financiera · No constituye asesoramiento regulado por la CNV · Argentina
    </div>
    """, unsafe_allow_html=True)
