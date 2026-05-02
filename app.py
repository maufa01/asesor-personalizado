"""
FinanzasIA — Asesor Financiero Inteligente
"""

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from datetime import datetime
from modules.ui_config import apply_custom_css, render_header, render_footer
from modules.profiler import render_profiler
from modules.portfolio import build_portfolio
from modules.charts import render_pie_chart, render_evolution_chart, render_bar_simulation, render_allocation_table, render_buy_guide
from modules.simulator import simulate_portfolio
from modules.ai_advisor import get_ai_analysis, get_rebalancing_advice, chat_with_advisor
from modules.glossary import render_glossary
from modules.costo_no_invertir import render_cost_of_not_investing, render_cost_results

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
    box.innerHTML = '<div style="font-size:4rem;margin-bottom:1rem;filter:drop-shadow(0 0 20px rgba(240,180,41,0.6))">🎉</div><h1 style="font-family:Syne,sans-serif;font-size:clamp(1.6rem,4vw,2.4rem);font-weight:800;color:#eef2ff;margin:0 0 0.8rem;line-height:1.2;letter-spacing:-0.02em;">¡Su cartera personalizada está lista!</h1><p style="font-family:DM Sans,sans-serif;font-size:clamp(0.95rem,2vw,1.15rem);color:#94a3b8;margin:0 0 1.5rem;">Análisis completado en menos de 2 minutos.</p><p style="font-size:0.8rem;color:#475569;">Toque en cualquier lugar para continuar</p>';
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

def init_state():
    defaults = {
        "step":        "intro",
        "profile":     None,
        "portfolio":   None,
        "simulation":  None,
        "ai_analysis": None,
        "chat_history": [],
        "answers":     {},
        "theme":       "dark",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()
apply_custom_css()
render_header()

# ── Sidebar: frescura de scores y botón de actualización ──────────────────────
def _score_age(path: str) -> str:
    p = Path(path)
    if not p.exists():
        return None, "⚫ No encontrado"
    delta = datetime.now() - datetime.fromtimestamp(p.stat().st_mtime)
    days  = delta.days
    hours = delta.seconds // 3600
    if days == 0:
        label = f"hace {hours}h" if hours > 0 else "hace menos de 1h"
        icon  = "🟢"
    elif days <= 3:
        label = f"hace {days}d"
        icon  = "🟢"
    elif days <= 7:
        label = f"hace {days}d"
        icon  = "🟡"
    else:
        label = f"hace {days}d — desactualizado"
        icon  = "🔴"
    return days, f"{icon} {label}"

with st.sidebar:
    st.markdown("### ⚙️ Scores de mercado")
    eq_days,   eq_label   = _score_age("finviz_scores.json")
    bond_days, bond_label = _score_age("bond_scores.json")
    st.markdown(f"**Equity / CEDEARs:** {eq_label}")
    st.markdown(f"**Bonos ARG:** {bond_label}")
    st.markdown("---")
    st.caption("Los scores determinan qué activos entran a tu cartera y con qué peso.")
    if st.button("🔄 Actualizar scores ahora", use_container_width=True):
        with st.spinner("Actualizando scores de equity... (~2 min)"):
            try:
                from modules.finviz_scorer import run_and_save as _run_eq
                _run_eq()
            except Exception as e:
                st.error(f"Error equity scorer: {e}")
        with st.spinner("Actualizando scores de bonos..."):
            try:
                from modules.bond_scorer import run_and_save as _run_bonds
                _run_bonds()
            except Exception as e:
                st.error(f"Error bond scorer: {e}")
        st.success("✅ Scores actualizados")
        st.rerun()

step = st.session_state.step

# ══════════════════════════════════════════════════════════════════════════════
# INTRO
# ══════════════════════════════════════════════════════════════════════════════
if step == "intro":
    st.markdown("""<div class="hero-card">
<div class="hero-icon">📊</div>
<h1 class="hero-title">Su asesor financiero digital<br>personalizado para Argentina</h1>
<p class="hero-subtitle">
Respondá un breve cuestionario sobre sus objetivos financieros.<br>
Nuestro sistema analizará su perfil y le sugerirá una cartera<br>
diversificada acorde a su situación.
</p>
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
<strong>¿Para quién es esta herramienta?</strong> Para cualquier persona en Argentina que desee optimizar su estrategia de inversión,
independientemente de su experiencia previa en el mercado de capitales.
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("¿Cuánto perdí por no invertir?", key="cost_btn", use_container_width=True):
        st.session_state.step = "costo_no_invertir"
        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Iniciar Evaluación", key="start_btn", use_container_width=True):
        st.session_state.step = "profiling"
        st.rerun()

    st.markdown("""<p class="disclaimer">
⚠️ Esta herramienta es de carácter educativo y no constituye asesoramiento financiero regulado por la CNV.
Consulte siempre con un asesor habilitado antes de tomar decisiones de inversión.
</p>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# COSTO DE NO INVERTIR
# ══════════════════════════════════════════════════════════════════════════════
elif step == "costo_no_invertir":
    render_cost_of_not_investing()

elif step == "cost_results":
    render_cost_results()

# ══════════════════════════════════════════════════════════════════════════════
# CUESTIONARIO
# ══════════════════════════════════════════════════════════════════════════════
elif step == "profiling":
    profile_data = render_profiler()

    if profile_data:
        st.session_state.profile = profile_data
        with st.spinner("Construyendo su cartera personalizada..."):
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

    # ── Resolución de moneda de display ──────────────────────────────────────
    _MEP_RATE      = 1200                                  # ARS/USD de referencia
    _currency_in   = profile.get("currency", "USD")       # moneda con que el usuario ingresó
    _capital_usd   = profile["capital"]                    # siempre en USD internamente
    _capital_orig  = profile.get("capital_original", _capital_usd)
    # Tasa efectiva usada al ingresar: capital_orig / capital_usd
    _fx_rate       = _capital_orig / _capital_usd if _currency_in == "ARS" else 1.0

    # Toggle (solo si el usuario ingresó en ARS)
    if _currency_in == "ARS":
        if "_display_currency" not in st.session_state:
            st.session_state._display_currency = "ARS"
        _tog_col, _ = st.columns([3, 5])
        with _tog_col:
            st.markdown('<div class="currency-toggle-wrap"><span class="currency-toggle-label">Ver cifras en:</span></div>', unsafe_allow_html=True)
            _disp_sel = st.radio(
                "Ver cifras en:", ["ARS (Pesos)", "USD (Dólares)"],
                horizontal=True, key="currency_toggle", label_visibility="collapsed",
            )
        st.session_state._display_currency = "ARS" if "ARS" in _disp_sel else "USD"

    _disp_curr = st.session_state.get("_display_currency", _currency_in)

    if _disp_curr == "ARS" and _currency_in == "ARS":
        _disp_factor  = _fx_rate
        _disp_capital = _capital_orig
        _disp_prefix  = "$"
        _disp_suffix  = " ARS"
    else:
        _disp_factor  = 1.0
        _disp_capital = _capital_usd
        _disp_prefix  = "USD "
        _disp_suffix  = ""

    st.markdown("""<a class="fab-btn" href="#chat-section"
onclick="document.getElementById('chat-section').scrollIntoView({behavior:'smooth'});return false;">
💬 Consultar al Asesor
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
        "conservador": "Usted prioriza la preservación del capital por encima del crecimiento. Su cartera apunta a proteger el patrimonio con bajo riesgo.",
        "estable":     "Usted desea un rendimiento superior al plazo fijo sin exponerse a caídas significativas. Su cartera combina dólares, bonos sólidos y algo de renta variable global.",
        "moderado":    "Usted busca un equilibrio entre crecimiento y protección patrimonial. Su cartera combina instrumentos seguros con activos de mayor rendimiento.",
        "agresivo":    "Usted está dispuesto a asumir mayor riesgo para maximizar el crecimiento a largo plazo. Su cartera apunta al mayor rendimiento posible.",
    }

    rc  = risk_colors.get(profile["risk_profile"], "#60a5fa")
    re  = risk_emojis.get(profile["risk_profile"], "🔵")
    rl  = risk_labels.get(profile["risk_profile"], profile["risk_profile"].upper())
    rex = risk_explanations.get(profile["risk_profile"], "")

    _disc_by_risk = {
        "conservador": "orientada a preservación de capital con bajo riesgo.",
        "estable":     "con exposición moderada a bonos y renta variable global.",
        "moderado":    "equilibrada entre seguridad y crecimiento; puede fluctuar en el corto plazo.",
        "agresivo":    "de alto crecimiento; puede sufrir caídas significativas en el corto plazo.",
    }
    _disc_text = _disc_by_risk.get(profile["risk_profile"], "")

    # ── Panel de resumen rápido ───────────────────────────────────────────────
    st.markdown(f"""<div class="summary-panel">
<div class="summary-top">
<div class="profile-pill" style="background:{rc}22;border:1.5px solid {rc};color:{rc};">
{re} {rl}
</div>
<h2 class="summary-title">Cartera Sugerida</h2>
<div class="explain-outer"><p class="summary-explain">{rex}</p></div>
<div class="legal-disclaimer">
  ⚠️ <strong>Aviso legal</strong> · Cartera {_disc_text}
  Capital: {_disp_prefix}{_disp_capital:,.0f}{_disp_suffix} · Horizonte: {profile['horizon']} años · Perfil: {rl}.
  Esta herramienta tiene fines educativos y no reemplaza el asesoramiento de un profesional regulado por la CNV.
</div>
</div>
<div class="summary-grid summary-main-grid">
<div class="summary-item">
<div class="si-label">Capital a invertir</div>
<div class="si-value">{_disp_prefix}{_disp_capital:,.0f}{_disp_suffix}</div>
</div>
<div class="summary-item">
<div class="si-label">Horizonte</div>
<div class="si-value">{profile['horizon']} años</div>
</div>
<div class="summary-item">
<div class="si-label">Retorno estimado/año</div>
<div class="si-value" style="color:#22c55e;">{portfolio['expected_cagr']*100:.1f}%</div>
<div class="si-sub">Rendimiento histórico esperado (base USD)</div>
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
<div class="si-label">Volatilidad estimada</div>
<div class="si-value" style="color:#f59e0b;">{portfolio['expected_volatility']*100:.1f}%</div>
</div>
</div>
</details>
<div class="summary-desc">{portfolio['summary']}</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Métricas de simulación ────────────────────────────────────────────────
    sim_data       = simulation["scenarios"]["base"]
    total_end_usd  = sim_data[-1]
    total_gain_usd = total_end_usd - _capital_usd
    cagr           = portfolio["expected_cagr"]
    vol            = portfolio["expected_volatility"]

    total_end_disp  = total_end_usd  * _disp_factor
    total_gain_disp = total_gain_usd * _disp_factor

    gain_color = "#22c55e" if total_gain_disp >= 0 else "#ef4444"
    sign       = "+" if total_gain_disp >= 0 else ""
    cagr_sub   = "Rendimiento histórico esperado (base USD)"

    st.markdown(f"""<div class="metrics-grid">
<div class="metric-card">
  <div class="metric-label">Retorno anual estimado</div>
  <div class="metric-value" style="color:#22c55e;">{cagr*100:.1f}%</div>
  <div class="metric-sub">{cagr_sub}</div>
</div>
<div class="metric-card">
  <div class="metric-label">Volatilidad estimada</div>
  <div class="metric-value" style="color:#f59e0b;">{vol*100:.1f}%</div>
  <div class="metric-sub">Fluctuación anual de la cartera</div>
</div>
<div class="metric-card">
  <div class="metric-label">Capital proyectado en {profile['horizon']}a</div>
  <div class="metric-value" style="color:#60a5fa;">{_disp_prefix}{total_end_disp:,.0f}{_disp_suffix}</div>
  <div class="metric-sub">Escenario base</div>
</div>
<div class="metric-card">
  <div class="metric-label">Ganancia estimada</div>
  <div class="metric-value" style="color:{gain_color};">{sign}{_disp_prefix}{abs(total_gain_disp):,.0f}{_disp_suffix}</div>
  <div class="metric-sub">Sobre el capital inicial</div>
</div>
</div>""", unsafe_allow_html=True)

    if _currency_in == "ARS":
        st.markdown(
            f'<p class="fx-rate-note">Tipo de cambio MEP de referencia: ${_fx_rate:,.0f} ARS/USD</p>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Distribución + Evolución ──────────────────────────────────────────────
    col_pie, col_evo = st.columns([1, 1.6])

    with col_pie:
        st.markdown('<div class="section-title">📊 Distribución de la Cartera</div>', unsafe_allow_html=True)
        render_pie_chart(portfolio)

    with col_evo:
        _scenario_headlines = {
            "conservador": "Preservación del capital con rendimiento consistente.",
            "estable":     "Rendimiento superior al plazo fijo con volatilidad controlada.",
            "moderado":    "Su capital tiene posibilidades reales de crecer a mediano plazo.",
            "agresivo":    "El riesgo asumido tiene su recompensa en el largo plazo.",
        }
        _headline = _scenario_headlines.get(profile["risk_profile"], "")
        st.markdown('<div class="section-title">📈 Proyección de Crecimiento</div>', unsafe_allow_html=True)
        st.markdown(f'<h3 class="chart-headline">{_headline}</h3>', unsafe_allow_html=True)
        # Pasar capital_original según la moneda seleccionada en el toggle
        _bar_cap_orig = _disp_capital if _disp_curr != _currency_in else profile.get("capital_original", _capital_usd)
        render_bar_simulation(portfolio, _capital_usd,
                              currency=_disp_curr,
                              capital_original=_bar_cap_orig)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabla de activos ──────────────────────────────────────────────────────
    st.markdown('<div class="section-title">📋 En qué está invertido su dinero</div>', unsafe_allow_html=True)
    render_allocation_table(portfolio, _disp_capital, currency_label=_disp_curr)

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

    # ── Guía de compra ────────────────────────────────────────────────────────
    render_buy_guide(portfolio)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Análisis IA ───────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">💬 Análisis Profesional</div>', unsafe_allow_html=True)

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
<p class="ai-empty-title">El análisis profesional de su cartera está disponible</p>
<div class="ai-empty-bullets">
<div class="ai-bullet">✓ Por qué esta cartera se adapta a su perfil</div>
<div class="ai-bullet">✓ Qué hacer cuando esté listo para invertir</div>
<div class="ai-bullet">✓ Alertas sobre riesgos que debe conocer</div>
</div>
</div>""", unsafe_allow_html=True)

        st.markdown('<div class="ai-cta-marker"></div>', unsafe_allow_html=True)

        _, col_cta, _ = st.columns([1, 2, 1])
        with col_cta:
            run_ai = st.button("Generar Análisis",
                               key="run_ai", use_container_width=True)

        if run_ai:
            with st.spinner("Generando análisis profesional..."):
                analysis = get_ai_analysis(profile, portfolio)
                st.session_state.ai_analysis = analysis
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── ¿Y ahora qué? ─────────────────────────────────────────────────────────
    st.markdown('<div class="section-title">❓ Próximos Pasos</div>', unsafe_allow_html=True)
    st.markdown("""<div class="action-guide">
<div class="action-step">
  <div class="action-step-number">1</div>
  <div class="action-step-body">
    <div class="action-step-title">Abra una cuenta en IOL o Balanz</div>
    <div class="action-step-copy">El proceso es gratuito y demora aproximadamente 10 minutos.</div>
    <details class="action-step-help"><summary>¿Cómo hacerlo?</summary>
      <div>Seleccione la plataforma, complete sus datos personales y verifique su identidad con DNI y selfie.</div>
    </details>
  </div>
</div>
<div class="action-step">
  <div class="action-step-number">2</div>
  <div class="action-step-body">
    <div class="action-step-title">Deposite el capital que desea invertir</div>
    <div class="action-step-copy">Transfiera desde su cuenta bancaria o billetera digital.</div>
    <details class="action-step-help"><summary>¿Cómo hacerlo?</summary>
      <div>Acceda a la opción de depósito o transferencia en la app y siga los pasos para enviar pesos o dólares.</div>
    </details>
  </div>
</div>
<div class="action-step">
  <div class="action-step-number">3</div>
  <div class="action-step-body">
    <div class="action-step-title">Adquiera los instrumentos de su cartera</div>
    <div class="action-step-copy">Respete la ponderación sugerida para cada instrumento.</div>
    <details class="action-step-help"><summary>¿Cómo hacerlo?</summary>
      <div>Seleccione cada instrumento, ingrese la cantidad y confirme la operación. Si tiene dudas, comience por el activo más conservador.</div>
    </details>
  </div>
</div>
<div class="action-step">
  <div class="action-step-number">4</div>
  <div class="action-step-body">
    <div class="action-step-title">Revise el rendimiento de su cartera mensualmente</div>
    <div class="action-step-copy">No es necesario monitorear la cartera a diario.</div>
    <details class="action-step-help"><summary>¿Cómo hacerlo?</summary>
      <div>Ingrese a su cuenta cada 30 días, verifique el rendimiento y ajuste solo si cambiaron sus objetivos o su situación financiera.</div>
    </details>
  </div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Chat con el asesor ────────────────────────────────────────────────────
    st.markdown('<div id="chat-section"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">💬 Consultas al Asesor</div>', unsafe_allow_html=True)

    chat_history = st.session_state.chat_history

    if chat_history:
        for msg in chat_history:
            is_user = msg["role"] == "user"
            align   = "chat-user" if is_user else "chat-advisor"
            label   = "Usted" if is_user else "Lucas · Asesor IA"
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
        with st.spinner("El asesor está procesando su consulta..."):
            answer = chat_with_advisor(user_input.strip(), chat_history, profile, portfolio)
        st.session_state.chat_history.append({"role": "user",      "content": user_input.strip()})
        st.session_state.chat_history.append({"role": "assistant", "content": answer})
        st.rerun()

    if chat_history:
        if st.button("🗑️ Limpiar chat", key="clear_chat"):
            st.session_state.chat_history = []
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Glosario CTA ──────────────────────────────────────────────────────────
    st.markdown("""<div class="glosario-cta">
<div class="glosario-cta-title">📚 ¿Hay algún término que no conoce?</div>
<p class="glosario-cta-sub">Consulte el Glosario Financiero con definiciones claras y ejemplos prácticos.</p>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_glos, col_r2, _ = st.columns([1, 1, 1])
    with col_glos:
        if st.button("📚 Ver Glosario", key="glosario_from_results", use_container_width=True):
            st.session_state._prev_step = "results"
            st.session_state.step = "glosario"
            st.rerun()
    with col_r2:
        if st.button("Nueva Evaluación", key="restart", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# GLOSARIO
# ══════════════════════════════════════════════════════════════════════════════
elif step == "glosario":
    render_glossary()

render_footer()
