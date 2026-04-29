"""
FinanzasIA — Asesor Financiero Inteligente
"""

import streamlit as st
import streamlit.components.v1 as components
from modules.ui_config import apply_custom_css, render_header, render_footer
from modules.profiler import render_profiler
from modules.portfolio import build_portfolio
from modules.charts import render_pie_chart, render_evolution_chart, render_bar_simulation, render_allocation_table
from modules.simulator import simulate_portfolio
from modules.ai_advisor import get_ai_analysis, get_rebalancing_advice, chat_with_advisor

_CELEBRATION_HTML = """<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
@keyframes confettiFall {
    0%   { transform: translateY(-10px) rotate(0deg);   opacity: 1; }
    100% { transform: translateY(110vh) rotate(720deg); opacity: 0; }
}
@keyframes celebFadeIn  { from { opacity:0; transform:scale(0.92); } to { opacity:1; transform:scale(1); } }
@keyframes celebFadeOut { from { opacity:1; } to { opacity:0; } }
</style>
</head><body style="margin:0;background:transparent;">
<script>
(function() {
    var LS_KEY = 'asesor_celebration_v1';
    try { if (window.parent.localStorage.getItem(LS_KEY)) return; } catch(e) {}
    var doc = window.parent.document;
    var overlay = doc.createElement('div');
    overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(5,8,16,0.93);z-index:99999;display:flex;flex-direction:column;align-items:center;justify-content:center;cursor:pointer;overflow:hidden;animation:celebFadeIn 0.4s ease-out both';
    var style = doc.createElement('style');
    style.textContent = '@keyframes confettiFall{0%{transform:translateY(-10px) rotate(0deg);opacity:1}100%{transform:translateY(110vh) rotate(720deg);opacity:0}}@keyframes celebFadeIn{from{opacity:0;transform:scale(0.92)}to{opacity:1;transform:scale(1)}}@keyframes celebFadeOut{from{opacity:1}to{opacity:0}}';
    doc.head.appendChild(style);
    var colors = ['#4fa3ff','#10d98a','#f0b429','#ff4d6a','#a78bfa','#ffffff','#38bdf8'];
    for (var i = 0; i < 70; i++) {
        var p = doc.createElement('div');
        var left = Math.random() * 100;
        var delay = Math.random() * 2.2;
        var dur = 2.2 + Math.random() * 1.8;
        var size = 5 + Math.random() * 9;
        var isRect = Math.random() > 0.5;
        p.style.cssText = 'position:absolute;left:' + left + '%;top:-20px;width:' + size + 'px;height:' + (isRect ? size * 0.4 : size) + 'px;background:' + colors[i % colors.length] + ';border-radius:' + (isRect ? '2px' : '50%') + ';animation:confettiFall ' + dur + 's ' + delay + 's ease-in forwards;pointer-events:none;';
        overlay.appendChild(p);
    }
    var box = doc.createElement('div');
    box.style.cssText = 'text-align:center;padding:2rem;position:relative;z-index:2;';
    box.innerHTML = '<div style="font-size:4rem;margin-bottom:1rem;filter:drop-shadow(0 0 20px rgba(240,180,41,0.6))">🎉</div><h1 style="font-family:Syne,sans-serif;font-size:clamp(1.6rem,4vw,2.4rem);font-weight:800;color:#eef2ff;margin:0 0 0.8rem;line-height:1.2;letter-spacing:-0.02em;">¡Ya está! Ahora sabés dónde poner tu plata 🎉</h1><p style="font-family:DM Sans,sans-serif;font-size:clamp(0.95rem,2vw,1.15rem);color:#94a3b8;margin:0 0 1.5rem;">Tu cartera está lista. Tomó menos de 2 minutos.</p><p style="font-size:0.8rem;color:#475569;">Tocá en cualquier lugar para continuar</p>';
    overlay.appendChild(box);
    doc.body.appendChild(overlay);
    try { window.parent.localStorage.setItem(LS_KEY, '1'); } catch(e) {}
    function dismiss() {
        overlay.style.animation = 'celebFadeOut 0.4s ease-in forwards';
        setTimeout(function() { overlay.remove(); style.remove(); }, 420);
    }
    overlay.addEventListener('click', dismiss);
    setTimeout(dismiss, 3000);
})();
</script></body></html>"""

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
<div class="hero-features">
<div class="hero-feature-pill"><span class="hero-feature-icon">🎯</span>Perfil personalizado</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">💼</span>Cartera sugerida</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">🤖</span>Análisis con IA</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">📈</span>Simulación de crecimiento</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">🇦🇷</span>Activos argentinos</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">💱</span>Opciones en pesos y USD</div>
</div>
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

        st.session_state.step             = "results"
        st.session_state.show_celebration = True
        st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# RESULTADOS
# ══════════════════════════════════════════════════════════════════════════════
elif step == "results":
    profile    = st.session_state.profile
    portfolio  = st.session_state.portfolio
    simulation = st.session_state.simulation

    st.markdown("""<a class="fab-btn" href="#chat-section"
onclick="document.getElementById('chat-section').scrollIntoView({behavior:'smooth'});return false;">
💬 Preguntale al asesor
</a>""", unsafe_allow_html=True)

    # ── Pantalla de celebración (primera vez) ─────────────────────────────────
    if st.session_state.get("show_celebration"):
        st.session_state.show_celebration = False
        components.html(_CELEBRATION_HTML, height=0)

    risk_colors = {
        "conservador": "#22c55e",
        "estable":     "#60a5fa",
        "moderado":    "#f59e0b",
        "agresivo":    "#ef4444",
    }
    risk_emojis = {"conservador": "🟢", "estable": "🔵", "moderado": "🟡", "agresivo": "🔴"}
    risk_labels = {
        "conservador": "Inversor Conservador",
        "estable":     "Inversor Estable",
        "moderado":    "Inversor Moderado",
        "agresivo":    "Inversor Agresivo",
    }
    risk_explanations = {
        "conservador": "Priorizás la seguridad de tu plata por encima del crecimiento. Tu cartera apunta a proteger el capital con bajo riesgo.",
        "estable":     "Querés algo mejor que un plazo fijo sin exponerte a grandes caídas. Tu cartera combina dólares, bonos sólidos y algo de acciones globales.",
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

    gain_color = "#22c55e" if total_gain >= 0 else "#ef4444"
    sign = "+" if total_gain >= 0 else ""
    st.markdown(f"""<div class="metrics-grid">
<div class="metric-card">
  <div class="metric-label">Retorno anual estimado</div>
  <div class="metric-value" style="color:#22c55e;">{cagr*100:.1f}%</div>
  <div class="metric-sub">Rendimiento esperado en USD</div>
</div>
<div class="metric-card">
  <div class="metric-label">¿Cuánto puede variar?</div>
  <div class="metric-value" style="color:#f59e0b;">{vol*100:.1f}%</div>
  <div class="metric-sub">Fluctuación anual estimada</div>
</div>
<div class="metric-card">
  <div class="metric-label">Capital proyectado en {profile['horizon']}a</div>
  <div class="metric-value" style="color:#60a5fa;">USD {total_end:,.0f}</div>
  <div class="metric-sub">Escenario base</div>
</div>
<div class="metric-card">
  <div class="metric-label">Ganancia estimada</div>
  <div class="metric-value" style="color:{gain_color};">{sign}USD {total_gain:,.0f}</div>
  <div class="metric-sub">Sobre el capital inicial</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Distribución + Evolución ──────────────────────────────────────────────
    col_pie, col_evo = st.columns([1, 1.6])

    with col_pie:
        st.markdown('<div class="section-title">📊 ¿Cómo se distribuye tu cartera?</div>', unsafe_allow_html=True)
        render_pie_chart(portfolio)

    with col_evo:
        _scenario_headlines = {
            "conservador": "En el peor caso, tu plata sigue valiendo lo mismo.",
            "estable":     "Más que un plazo fijo, menos sustos que la bolsa.",
            "moderado":    "Tu plata tiene chances reales de crecer.",
            "agresivo":    "El riesgo tiene su recompensa a largo plazo.",
        }
        _headline = _scenario_headlines.get(profile["risk_profile"], "")
        st.markdown('<div class="section-title">📈 ¿Cuánto puede crecer tu plata?</div>', unsafe_allow_html=True)
        st.markdown(f'<h3 class="chart-headline">{_headline}</h3>', unsafe_allow_html=True)
        render_bar_simulation(portfolio, profile["capital"],
                              currency=profile.get("currency", "USD"),
                              capital_original=profile.get("capital_original", profile["capital"]))

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabla de activos ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📋 Activos de tu cartera</div>', unsafe_allow_html=True)
    render_allocation_table(portfolio, profile["capital"])

    # ── Advertencias de solapamiento ──────────────────────────────────────────
    overlaps = portfolio.get("overlaps", [])
    if overlaps:
        st.markdown("<br>", unsafe_allow_html=True)
        for ov in overlaps:
            etf = ov["etf"].upper()
            conflicts = ", ".join(c.upper() for c in ov["conflicts"])
            reason = ov["reason"]
            st.markdown(f"""<div class="alert-card alert-medium">
<span class="alert-icon">⚠️</span>
<div><strong>Solapamiento detectado: {etf} + {conflicts}</strong><br>
<span>{reason}</span></div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Análisis IA ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">💬 Tu análisis personalizado</div>', unsafe_allow_html=True)

    if st.session_state.ai_analysis:
        col_ai1, col_ai2 = st.columns([3, 1])
        with col_ai2:
            if st.button("🗑️ Limpiar análisis", key="clear_ai", use_container_width=True):
                st.session_state.ai_analysis = None
                st.rerun()

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
        st.markdown("""<div class="ai-empty-state">
<div class="ai-empty-icon">✨</div>
<p class="ai-empty-title">Tu asesor personal está listo para ayudarte</p>
<div class="ai-empty-bullets">
<div class="ai-bullet">✓ Por qué esta cartera se adapta a vos</div>
<div class="ai-bullet">✓ Qué hacer primero cuando estés listo para invertir</div>
<div class="ai-bullet">✓ Alertas sobre riesgos que deberías saber</div>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="ai-cta-marker"></div>', unsafe_allow_html=True)

        _, col_cta, _ = st.columns([1, 2, 1])
        with col_cta:
            run_ai = st.button("✨ Generar mi análisis personalizado",
                               key="run_ai", use_container_width=True)

        if run_ai:
            with st.spinner("Analizando tu cartera..."):
                analysis = get_ai_analysis(profile, portfolio)
                st.session_state.ai_analysis = analysis
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ¿Y ahora qué? ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">❓ ¿Y ahora qué?</div>', unsafe_allow_html=True)
    st.markdown("""<div class="action-guide">
<div class="action-step">
  <div class="action-step-number">1</div>
  <div class="action-step-body">
    <div class="action-step-title">Abrí una cuenta en IOL o Balanz</div>
    <div class="action-step-copy">Es gratis y tarda 10 minutos.</div>
    <details class="action-step-help"><summary>¿Cómo hago esto?</summary>
      <div>Elegí la plataforma, completá los datos personales y verificá tu identidad con DNI y selfie.</div>
    </details>
  </div>
</div>
<div class="action-step">
  <div class="action-step-number">2</div>
  <div class="action-step-body">
    <div class="action-step-title">Depositá el dinero que querés invertir</div>
    <div class="action-step-copy">Transferí desde tu cuenta bancaria o billetera digital.</div>
    <details class="action-step-help"><summary>¿Cómo hago esto?</summary>
      <div>Buscá la opción de depósito o transferencia en la app y seguí los pasos para enviar pesos o dólares.</div>
    </details>
  </div>
</div>
<div class="action-step">
  <div class="action-step-number">3</div>
  <div class="action-step-body">
    <div class="action-step-title">Comprá los activos de tu cartera uno por uno</div>
    <div class="action-step-copy">Seguí la proporción recomendada en cada activo.</div>
    <details class="action-step-help"><summary>¿Cómo hago esto?</summary>
      <div>Seleccioná cada activo, ingresá la cantidad y confirmá la compra. Si no estás seguro, empezá con el activo más seguro.</div>
    </details>
  </div>
</div>
<div class="action-step">
  <div class="action-step-number">4</div>
  <div class="action-step-body">
    <div class="action-step-title">Revisá cómo va tu plata una vez por mes</div>
    <div class="action-step-copy">No hace falta mirar todos los días.</div>
    <details class="action-step-help"><summary>¿Cómo hago esto?</summary>
      <div>Entrá a tu cuenta cada 30 días, verificá el rendimiento y ajustá solo si cambió tu objetivo o tu presupuesto.</div>
    </details>
  </div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chat con el asesor ────────────────────────────────────────────────────
    st.markdown('<div id="chat-section"></div>', unsafe_allow_html=True)
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
