"""
FinanzasIA — Asesor Financiero Inteligente
"""

import streamlit as st
from modules.ui_config import apply_custom_css, render_header, render_footer
from modules.profiler import render_profiler
from modules.portfolio import build_portfolio
from modules.charts import render_pie_chart, render_evolution_chart, render_bar_simulation, render_allocation_table
from modules.simulator import simulate_portfolio
from modules.ai_advisor import get_ai_analysis, get_rebalancing_advice, chat_with_advisor

st.set_page_config(
    page_title="FinanzasIA · Tu asesor financiero",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_custom_css()


def init_state():
    defaults = {
        "step":        "intro",
        "profile":     None,
        "portfolio":   None,
        "simulation":  None,
        "ai_analysis": None,
        "chat_history": [],
        "answers":     {},
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()
render_header()

step = st.session_state.step

# ══════════════════════════════════════════════════════════════════════════════
# INTRO
# ══════════════════════════════════════════════════════════════════════════════
if step == "intro":
    st.markdown("""<div class="hero-card">
<div class="hero-icon">📊</div>
<h1 class="hero-title">Invertí mejor tu plata<br>con un asesor que te escucha</h1>
<p class="hero-subtitle">
Respondé 6 preguntas simples. En menos de 2 minutos te armamos<br>
una cartera de inversión adaptada a vos, explicada en lenguaje simple.
</p>
<p class="hero-human-copy">No importa si nunca invertiste antes — te explicamos todo en lenguaje simple.</p>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""<div class="audience-note">
<strong>¿Para quién es esto?</strong> Para cualquier persona en Argentina que quiera invertir mejor su plata,
aunque nunca haya invertido antes. No necesitás saber nada de finanzas.
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🚀 Empezar ahora — son solo 6 preguntas", key="start_btn", use_container_width=True):
        st.session_state.step = "profiling"
        st.rerun()

    st.markdown("""<p class="disclaimer">
⚠️ Esta aplicación es educativa y no constituye asesoramiento financiero profesional.
Consultá siempre con un asesor habilitado antes de invertir dinero real.
</p>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# CUESTIONARIO
# ══════════════════════════════════════════════════════════════════════════════
elif step == "profiling":
    profile_data = render_profiler()

    if profile_data:
        st.session_state.profile = profile_data
        with st.spinner("Armando tu cartera personalizada..."):
            portfolio  = build_portfolio(profile_data)
            simulation = simulate_portfolio(
                portfolio,
                years=profile_data["horizon"],
                initial_capital=profile_data["capital"],
            )
            st.session_state.portfolio  = portfolio
            st.session_state.simulation = simulation

        st.session_state.step = "results"
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# RESULTADOS
# ══════════════════════════════════════════════════════════════════════════════
elif step == "results":
    profile    = st.session_state.profile
    portfolio  = st.session_state.portfolio
    simulation = st.session_state.simulation

    risk_colors = {"conservador": "#22c55e", "moderado": "#f59e0b", "agresivo": "#ef4444"}
    risk_emojis = {"conservador": "🟢", "moderado": "🟡", "agresivo": "🔴"}
    risk_labels = {
        "conservador": "Inversor Conservador",
        "moderado":    "Inversor Moderado",
        "agresivo":    "Inversor Agresivo",
    }
    risk_explanations = {
        "conservador": "Priorizás la seguridad de tu plata por encima del crecimiento. Tu cartera apunta a proteger el capital con bajo riesgo.",
        "moderado":    "Buscás un equilibrio entre hacer crecer tu plata y no arriesgar demasiado. Tu cartera mezcla seguridad con crecimiento.",
        "agresivo":    "Estás dispuesto a asumir riesgo para buscar mayor crecimiento a largo plazo. Tu cartera apunta al máximo rendimiento posible.",
    }

    rc  = risk_colors.get(profile["risk_profile"], "#60a5fa")
    re  = risk_emojis.get(profile["risk_profile"], "🔵")
    rl  = risk_labels.get(profile["risk_profile"], profile["risk_profile"].upper())
    rex = risk_explanations.get(profile["risk_profile"], "")

    # ── Panel de resumen rápido ───────────────────────────────────────────────
    st.markdown(f"""<div class="summary-panel">
<div class="summary-top">
<div class="profile-pill" style="background:{rc}22;border:1.5px solid {rc};color:{rc};">
{re} {rl}
</div>
<h2 class="summary-title">Tu cartera sugerida está lista</h2>
<p class="summary-explain">{rex}</p>
</div>
<div class="summary-grid summary-main-grid">
<div class="summary-item">
<div class="si-label">Capital a invertir</div>
<div class="si-value">{profile.get('capital_display', f"USD {profile['capital']:,.0f}")}</div>
</div>
<div class="summary-item">
<div class="si-label">Horizonte</div>
<div class="si-value">{profile['horizon']} años</div>
</div>
<div class="summary-item">
<div class="si-label">Retorno estimado/año</div>
<div class="si-value" style="color:#22c55e;">{portfolio['expected_cagr']*100:.1f}%</div>
<div class="si-sub">Promedio ponderado de tu cartera en USD</div>
</div>
</div>
<details class="summary-detail">
<summary class="summary-detail-btn">Ver detalle completo</summary>
<div class="summary-grid summary-detail-grid">
<div class="summary-item">
<div class="si-label">Activos en la cartera</div>
<div class="si-value">{len(portfolio['positions'])}</div>
</div>
<div class="summary-item">
<div class="si-label">En pesos ARS</div>
<div class="si-value" style="color:#a3e635;">{portfolio['pesos_pct']:.0f}%</div>
</div>
<div class="summary-item">
<div class="si-label">En dólares USD</div>
<div class="si-value" style="color:#38bdf8;">{portfolio['usd_pct']:.0f}%</div>
</div>
<div class="summary-item">
<div class="si-label">Diversificación</div>
<div class="si-value">{portfolio['diversification'].upper()}</div>
</div>
<div class="summary-item">
<div class="si-label">¿Cuánto puede variar tu plata?</div>
<div class="si-value" style="color:#f59e0b;">{portfolio['expected_volatility']*100:.1f}%</div>
</div>
</div>
</details>
<div class="summary-desc">{portfolio['summary']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Métricas de simulación ────────────────────────────────────────────────
    sim_data    = simulation["scenarios"]["base"]
    total_end   = sim_data[-1]
    total_gain  = total_end - profile["capital"]
    cagr        = portfolio["expected_cagr"]
    vol         = portfolio["expected_volatility"]

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(f"""<div class="metric-card">
<div class="metric-label">Retorno anual estimado</div>
<div class="metric-value" style="color:#22c55e;">{cagr*100:.1f}%</div>
<div class="metric-sub">Rendimiento esperado en USD</div>
</div>""", unsafe_allow_html=True)
    with m2:
        st.markdown(f"""<div class="metric-card">
<div class="metric-label">¿Cuánto puede variar?</div>
<div class="metric-value" style="color:#f59e0b;">{vol*100:.1f}%</div>
<div class="metric-sub">Fluctuación anual estimada</div>
</div>""", unsafe_allow_html=True)
    with m3:
        st.markdown(f"""<div class="metric-card">
<div class="metric-label">Capital proyectado en {profile['horizon']}a</div>
<div class="metric-value" style="color:#60a5fa;">USD {total_end:,.0f}</div>
<div class="metric-sub">Escenario base</div>
</div>""", unsafe_allow_html=True)
    with m4:
        gain_color = "#22c55e" if total_gain >= 0 else "#ef4444"
        sign = "+" if total_gain >= 0 else ""
        st.markdown(f"""<div class="metric-card">
<div class="metric-label">Ganancia estimada</div>
<div class="metric-value" style="color:{gain_color};">{sign}USD {total_gain:,.0f}</div>
<div class="metric-sub">Sobre el capital inicial</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Distribución + Evolución ──────────────────────────────────────────────
    col_pie, col_evo = st.columns([1, 1.6])

    with col_pie:
        st.markdown('<div class="section-title">📊 ¿Cómo se distribuye tu cartera?</div>', unsafe_allow_html=True)
        render_pie_chart(portfolio)

    with col_evo:
        st.markdown('<div class="section-title">📈 ¿Cuánto puede crecer tu plata?</div>', unsafe_allow_html=True)
        render_bar_simulation(portfolio, profile["capital"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabla de activos ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📋 Activos de tu cartera</div>', unsafe_allow_html=True)
    render_allocation_table(portfolio, profile["capital"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Análisis IA ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">🤖 Análisis del asesor IA</div>', unsafe_allow_html=True)

    col_ai1, col_ai2 = st.columns([3, 1])
    with col_ai2:
        run_ai = st.button("✨ Generar análisis IA", key="run_ai", use_container_width=True)
        if st.session_state.ai_analysis:
            if st.button("🗑️ Limpiar análisis", key="clear_ai", use_container_width=True):
                st.session_state.ai_analysis = None
                st.rerun()

    if run_ai:
        with st.spinner("La IA está analizando tu cartera..."):
            analysis = get_ai_analysis(profile, portfolio)
            st.session_state.ai_analysis = analysis
            st.rerun()

    if st.session_state.ai_analysis:
        analysis = st.session_state.ai_analysis
        tabs = st.tabs(["📝 Por qué esta cartera", "⚠️ Alertas de riesgo", "🔄 Cuándo rebalancear", "💡 Consejos"])

        with tabs[0]:
            st.markdown(f'<div class="ai-response">{analysis["justification"]}</div>', unsafe_allow_html=True)
        with tabs[1]:
            alerts = analysis.get("alerts", [])
            if alerts:
                for alert in alerts:
                    severity = alert.get("severity", "medium")
                    icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(severity, "🔵")
                    st.markdown(f"""<div class="alert-card alert-{severity}">
<span class="alert-icon">{icon}</span>
<div><strong>{alert['title']}</strong><br><span>{alert['message']}</span></div>
</div>""", unsafe_allow_html=True)
            else:
                st.success("✅ No se detectaron alertas de riesgo significativas.")
        with tabs[2]:
            st.markdown(f'<div class="ai-response">{analysis["rebalancing"]}</div>', unsafe_allow_html=True)
        with tabs[3]:
            st.markdown(f'<div class="ai-response">{analysis["tips"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown("""<div class="ai-placeholder">
<div class="ai-placeholder-icon">🤖</div>
<p>Hacé clic en <strong>"Generar análisis IA"</strong> para recibir una explicación personalizada
de tu cartera en lenguaje simple, con alertas y consejos concretos.</p>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chat con el asesor ────────────────────────────────────────────────────
    st.markdown('<div class="section-title">💬 Preguntale al asesor</div>', unsafe_allow_html=True)

    chat_history = st.session_state.chat_history

    if chat_history:
        for msg in chat_history:
            is_user = msg["role"] == "user"
            align   = "chat-user" if is_user else "chat-advisor"
            label   = "Vos" if is_user else "Lucas · Asesor IA"
            st.markdown(
                f'<div class="chat-bubble {align}"><div class="chat-label">{label}</div>'
                f'<div class="chat-text">{msg["content"]}</div></div>',
                unsafe_allow_html=True,
            )

    with st.form("chat_form", clear_on_submit=True):
        col_inp, col_btn = st.columns([5, 1])
        with col_inp:
            user_input = st.text_input(
                "Pregunta",
                placeholder="Ej: ¿Qué es exactamente una LECAP? ¿Cómo compro el dólar MEP?",
                label_visibility="collapsed",
            )
        with col_btn:
            send = st.form_submit_button("Enviar", use_container_width=True)

    if send and user_input.strip():
        with st.spinner("Lucas está respondiendo..."):
            answer = chat_with_advisor(user_input.strip(), chat_history, profile, portfolio)
        st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if chat_history:
        if st.button("🗑️ Limpiar chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Reiniciar ─────────────────────────────────────────────────────────────
    _, col_r2, _ = st.columns([1, 1, 1])
    with col_r2:
        if st.button("🔁 Empezar de nuevo", key="restart", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

render_footer()
