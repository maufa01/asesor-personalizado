"""
FinanzasIA — Asesor Financiero Inteligente
"""

import threading

import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from datetime import datetime
from modules.ui_config import apply_custom_css, render_header, render_footer
from modules.profiler import render_profiler
from modules.portfolio import build_portfolio
from modules.charts import render_pie_chart, render_evolution_chart, render_bar_simulation, render_allocation_table, render_buy_guide
from modules.simulator import simulate_portfolio, comparar_vs_alternativas, proyectar_con_aportes
from modules.ai_advisor import get_ai_analysis, get_rebalancing_advice, chat_with_advisor
from modules.glossary import render_glossary
from modules.costo_no_invertir import render_cost_of_not_investing, render_cost_results
from modules.methodology import render_methodology

_SCORES_MAX_AGE_DAYS = 7   # umbral para auto-actualización


# ── Estado de actualización en segundo plano (persiste entre reruns) ──────────
@st.cache_resource
def _update_state():
    return {"thread": None, "last_result": None}


def _run_scores_background():
    """Descarga fundamentals y recalcula scores. Corre en hilo daemon."""
    errors = []
    try:
        from modules.finviz_scorer import run_and_save as _eq
        _eq()
    except Exception as e:
        errors.append(f"equity: {e}")
    try:
        from modules.bond_scorer import run_and_save as _bonds
        _bonds()
    except Exception as e:
        errors.append(f"bonos: {e}")
    _update_state()["last_result"] = "error" if errors else "ok"


def _score_age(path: str):
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


def _auto_update_if_stale() -> bool:
    """Dispara actualización en hilo de fondo si los scores tienen > 7 días. Retorna True si arrancó."""
    eq_days, _ = _score_age("finviz_scores.json")
    if eq_days is None or eq_days > _SCORES_MAX_AGE_DAYS:
        state = _update_state()
        t = state.get("thread")
        if t is None or not t.is_alive():
            thread = threading.Thread(target=_run_scores_background, daemon=True)
            thread.start()
            state["thread"] = thread
            state["last_result"] = None
            return True
    return False

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
        "step":                  "intro",
        "profile":               None,
        "portfolio":             None,
        "simulation":            None,
        "ai_analysis":           None,
        "chat_history":          [],
        "answers":               {},
        "theme":                 "dark",
        "auto_update_checked":   False,
        "scores_refreshed":      False,   # True cuando la actualización en curso termina
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# ── Auto-actualización de scores (una sola vez por sesión) ───────────────────
if not st.session_state.auto_update_checked:
    st.session_state.auto_update_checked = True
    _auto_update_if_stale()

# Detectar si el hilo de fondo acaba de terminar
_state = _update_state()
_bg_thread = _state.get("thread")
if (_bg_thread is not None
        and not _bg_thread.is_alive()
        and _state.get("last_result") == "ok"
        and not st.session_state.scores_refreshed):
    st.session_state.scores_refreshed = True

apply_custom_css()
render_header()

# ── Sidebar: frescura de scores y botón de actualización ──────────────────────

with st.sidebar:
    st.markdown("### ⚙️ Scores de mercado")
    eq_days,   eq_label   = _score_age("finviz_scores.json")
    bond_days, bond_label = _score_age("bond_scores.json")
    st.markdown(f"**Equity / CEDEARs:** {eq_label}")
    st.markdown(f"**Bonos ARG:** {bond_label}")

    # Tipo de cambio MEP en vivo
    try:
        from modules.market_data import get_mep_rate as _sidebar_mep
        _live_mep = _sidebar_mep()
        st.markdown(f"**MEP (bolsa):** ${_live_mep:,.0f} ARS/USD")
    except Exception:
        pass

    # Estado del hilo de fondo
    _bg = _update_state().get("thread")
    if _bg is not None and _bg.is_alive():
        st.info("⏳ Actualizando scores en segundo plano…")
    elif st.session_state.scores_refreshed:
        st.success("✅ Scores actualizados")

    st.markdown("---")
    st.caption("Los scores se actualizan automáticamente cuando tienen más de 7 días.")
    if st.button("🔄 Actualizar ahora", use_container_width=True):
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
        st.session_state.scores_refreshed = True
        st.success("✅ Scores actualizados")
        st.rerun()

    # Modo avanzado — solo para el administrador de la app
    with st.expander("⚙️ Avanzado", expanded=False):
        st.session_state["_modo_avanzado"] = st.checkbox(
            "Modo presentación académica",
            value=st.session_state.get("_modo_avanzado", False),
        )
        if st.session_state.get("_modo_avanzado"):
            if st.button("🎓 Metodología del sistema", use_container_width=True):
                st.session_state._prev_step = st.session_state.get("step", "intro")
                st.session_state.step = "metodologia"
                st.rerun()

step = st.session_state.step

# ══════════════════════════════════════════════════════════════════════════════
# INTRO
# ══════════════════════════════════════════════════════════════════════════════
if step == "intro":
    st.markdown("""<div class="hero-card">
<div class="hero-icon">🤝</div>
<h1 class="hero-title">Tu plata puede trabajar para vos.<br>Sin letra chica. Sin tecnicismos.</h1>
<p class="hero-subtitle">
Si alguna vez sentiste que invertir es solo para gente que sabe,<br>
o que ya te quemaste antes y no querés volver a pasar por eso —<br>
<strong>esta herramienta es para vos.</strong>
</p>
<div class="hero-features">
<div class="hero-feature-pill"><span class="hero-feature-icon">✅</span>Sin conocimientos previos</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">🛡️</span>Sin venderte nada</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">🇦🇷</span>Pensado para Argentina</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">⏱️</span>5 minutos y tenés tu cartera</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">💬</span>Te explicamos cada decisión</div>
<div class="hero-feature-pill"><span class="hero-feature-icon">🔒</span>Educativo, no asesoramiento</div>
</div>
</div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""<div class="audience-note">
<strong>¿Qué hace esta herramienta?</strong> Analizamos tu situación en 5 minutos y te mostramos
cómo podría estar invertida tu plata — qué instrumentos, en qué proporción y por qué cada uno.
Vos después decidís si querés avanzar con un asesor real. Acá solo entendés tus opciones.
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
    try:
        from modules.market_data import get_mep_rate as _get_mep
        _MEP_RATE = _get_mep()
    except Exception:
        _MEP_RATE = 1200                                   # fallback estático
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

    # ── Aviso de scores actualizados en esta sesión ───────────────────────────
    if st.session_state.scores_refreshed and not st.session_state.get("refresh_banner_dismissed"):
        col_b1, col_b2 = st.columns([5, 1])
        with col_b1:
            st.info("Los datos de mercado fueron actualizados. Podés generar una nueva evaluación para reflejar los últimos fundamentals.")
        with col_b2:
            if st.button("Recalcular", key="recalc_btn", use_container_width=True):
                st.session_state.refresh_banner_dismissed = True
                keys_to_clear = ["portfolio", "simulation", "ai_analysis", "chat_history", "show_celebration"]
                for k in keys_to_clear:
                    st.session_state[k] = None if k != "chat_history" else []
                st.session_state.step = "profiling"
                st.rerun()

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
            f'<p class="fx-rate-note">Tipo de cambio MEP: ${_MEP_RATE:,.0f} ARS/USD · '
            f'<span style="font-size:0.8em;opacity:0.7;">actualizado en tiempo real · '
            f'tasa usada al ingresar: ${_fx_rate:,.0f}</span></p>',
            unsafe_allow_html=True,
        )

    # ── Métricas cuantitativas — solo modo avanzado ───────────────────────────
    if st.session_state.get("_modo_avanzado"):
        _beta   = portfolio.get("beta_portfolio", 0)
        _sharpe = portfolio.get("sharpe_ratio", 0)
        _hhi    = portfolio.get("hhi", 0)
        _hhi_lb = portfolio.get("hhi_label", "")
        _avgsco = portfolio.get("avg_score")

        _beta_color   = "#22c55e" if _beta < 1.0 else ("#f59e0b" if _beta < 1.3 else "#ef4444")
        _sharpe_color = "#22c55e" if _sharpe >= 0.5 else ("#f59e0b" if _sharpe >= 0 else "#ef4444")
        _hhi_color    = "#22c55e" if _hhi < 0.15 else ("#f59e0b" if _hhi < 0.25 else "#ef4444")

        with st.expander("📐 Métricas cuantitativas del portafolio", expanded=True):
            st.markdown(f"""<div class="metrics-grid">
<div class="metric-card">
  <div class="metric-label">Beta del portafolio</div>
  <div class="metric-value" style="color:{_beta_color};">{_beta:.2f}</div>
  <div class="metric-sub">Sensibilidad al mercado (1.0 = neutral)</div>
</div>
<div class="metric-card">
  <div class="metric-label">Sharpe Ratio estimado</div>
  <div class="metric-value" style="color:{_sharpe_color};">{_sharpe:.2f}</div>
  <div class="metric-sub">Retorno ajustado por riesgo (rf = 4.5%)</div>
</div>
<div class="metric-card">
  <div class="metric-label">Índice HHI (concentración)</div>
  <div class="metric-value" style="color:{_hhi_color};">{_hhi:.3f}</div>
  <div class="metric-sub">{_hhi_lb} — 0 = perfecto, 1 = todo en un activo</div>
</div>
{f'<div class="metric-card"><div class="metric-label">Score promedio ponderado</div><div class="metric-value" style="color:#a78bfa;">{_avgsco}/100</div><div class="metric-sub">Calidad fundamental de los activos scorables</div></div>' if _avgsco else ""}
</div>""", unsafe_allow_html=True)
            st.caption("Beta: ponderado por betas Finviz. Sharpe: (CAGR − 4.5%) / σ. HHI: Herfindahl-Hirschman. Pesos equity optimizados con Markowitz (scipy).")

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

    # ── Tabla de activos + razón por activo ──────────────────────────────────
    st.markdown('<div class="section-title">📋 En qué está tu plata y por qué</div>', unsafe_allow_html=True)
    render_allocation_table(portfolio, _disp_capital, currency_label=_disp_curr)

    # ── Análisis fundamental por activo (solo modo avanzado) ─────────────────
    _scored = [p for p in portfolio["positions"] if p.get("score") and p.get("bloques")]
    if _scored and st.session_state.get("_modo_avanzado"):
        with st.expander(f"🔬 Análisis fundamental detallado ({len(_scored)} activos con score Finviz)", expanded=False):
            st.caption("Score calculado sobre 5 bloques: Valuación (25) + Calidad (25) + Solvencia (20) + Crecimiento (20) + Cualitativo (10) = 100 pts")
            for pos in sorted(_scored, key=lambda x: x.get("score", 0), reverse=True):
                bloques = pos["bloques"]
                ratios  = pos.get("ratios", {})
                sc      = pos["score"]
                rating_color = {"STRONG BUY": "#22c55e", "BUY": "#4fa3ff", "HOLD": "#f59e0b",
                                "UNDERWEIGHT": "#f97316", "AVOID": "#ef4444"}.get(
                    "STRONG BUY" if sc >= 85 else ("BUY" if sc >= 70 else ("HOLD" if sc >= 55 else ("UNDERWEIGHT" if sc >= 40 else "AVOID"))), "#94a3b8")
                rating_label = "STRONG BUY" if sc >= 85 else ("BUY" if sc >= 70 else ("HOLD" if sc >= 55 else ("UNDERWEIGHT" if sc >= 40 else "AVOID")))

                col_name, col_score, col_bars = st.columns([2, 1, 3])
                with col_name:
                    st.markdown(f"**{pos['name']}**  \n`{pos.get('ticker','')}`  \n_{pos.get('sector_framework', pos.get('sub',''))}_")
                with col_score:
                    st.markdown(f"<div style='font-size:1.8rem;font-weight:800;color:{rating_color};'>{sc}</div><div style='font-size:0.75rem;color:{rating_color};'>{rating_label}</div>", unsafe_allow_html=True)
                with col_bars:
                    b = bloques
                    st.markdown(f"""
<div style='font-size:0.8rem;line-height:1.8;'>
<span style='opacity:0.6;'>Valuación</span> <b>{b.get('valuacion',0)}/25</b> &nbsp;
<span style='opacity:0.6;'>Calidad</span> <b>{b.get('calidad',0)}/25</b> &nbsp;
<span style='opacity:0.6;'>Solvencia</span> <b>{b.get('solvencia',0)}/20</b> &nbsp;
<span style='opacity:0.6;'>Crecimiento</span> <b>{b.get('crecimiento',0)}/20</b> &nbsp;
<span style='opacity:0.6;'>Cualitativo</span> <b>{b.get('cualitativo',0)}/10</b>
</div>""", unsafe_allow_html=True)
                    # Ratios clave en una línea
                    r_items = []
                    if ratios.get("forward_pe"):    r_items.append(f"P/E fwd: {ratios['forward_pe']:.1f}×")
                    if ratios.get("roe"):           r_items.append(f"ROE: {ratios['roe']:.1f}%")
                    if ratios.get("margen_neto"):   r_items.append(f"Margen: {ratios['margen_neto']:.1f}%")
                    if ratios.get("eps_cagr_5y"):   r_items.append(f"EPS CAGR 5y: {ratios['eps_cagr_5y']:.1f}%")
                    if ratios.get("deuda_equity"):  r_items.append(f"D/E: {ratios['deuda_equity']:.2f}×")
                    if r_items:
                        st.caption(" · ".join(r_items))
                st.divider()

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

    # ── ¿Qué pasa si no hacés nada? ───────────────────────────────────────────
    st.markdown('<div class="section-title">📊 ¿Qué pasa con tu plata si no la invertís?</div>', unsafe_allow_html=True)
    st.caption("Comparación en dólares reales a lo largo del tiempo. El plazo fijo rinde ~1% real anual en dólares. Los dólares guardados pierden poder adquisitivo con la inflación global.")

    _comp = comparar_vs_alternativas(_capital_usd, profile["horizon"], portfolio["expected_cagr"])
    _cp_f = _comp["portfolio_final"] * _disp_factor
    _cp_pf = _comp["pf_final"] * _disp_factor
    _cp_col = _comp["colchon_final"] * _disp_factor
    _dif_pf  = (_comp["diferencia_vs_pf"]) * _disp_factor
    _dif_col = (_comp["diferencia_vs_colchon"]) * _disp_factor

    st.markdown(f"""<div class="metrics-grid">
<div class="metric-card">
  <div class="metric-label">Esta cartera en {profile['horizon']} años</div>
  <div class="metric-value" style="color:#22c55e;">{_disp_prefix}{_cp_f:,.0f}{_disp_suffix}</div>
  <div class="metric-sub">Rendimiento estimado {portfolio['expected_cagr']*100:.1f}% anual</div>
</div>
<div class="metric-card">
  <div class="metric-label">Solo plazo fijo en {profile['horizon']} años</div>
  <div class="metric-value" style="color:#f59e0b;">{_disp_prefix}{_cp_pf:,.0f}{_disp_suffix}</div>
  <div class="metric-sub">~1% real anual en dólares (históricamente)</div>
</div>
<div class="metric-card">
  <div class="metric-label">Dólares guardados en {profile['horizon']} años</div>
  <div class="metric-value" style="color:#ef4444;">{_disp_prefix}{_cp_col:,.0f}{_disp_suffix}</div>
  <div class="metric-sub">Pierden ~2.5% por año contra la inflación global</div>
</div>
<div class="metric-card">
  <div class="metric-label">Lo que ganás vs dejarlo parado</div>
  <div class="metric-value" style="color:#a78bfa;">{_disp_prefix}{_dif_col:,.0f}{_disp_suffix}</div>
  <div class="metric-sub">Diferencia real a {profile['horizon']} años vs dólares sin invertir</div>
</div>
</div>""", unsafe_allow_html=True)

    # Gráfico de comparación — Plotly para controlar eje Y
    try:
        import plotly.graph_objects as _go
        _years_ax  = _comp["years"]
        _port_vals = [v * _disp_factor for v in _comp["portfolio"]]
        _pf_vals   = [v * _disp_factor for v in _comp["pf"]]
        _col_vals  = [v * _disp_factor for v in _comp["colchon"]]

        _y_min = min(_col_vals) * 0.97
        _y_max = max(_port_vals) * 1.03

        _fig_comp = _go.Figure()
        _fig_comp.add_trace(_go.Scatter(
            x=_years_ax, y=_port_vals,
            name="Esta cartera", mode="lines",
            line=dict(color="#22c55e", width=3),
            fill="tonexty" if False else None,
        ))
        _fig_comp.add_trace(_go.Scatter(
            x=_years_ax, y=_pf_vals,
            name="Plazo fijo", mode="lines",
            line=dict(color="#f59e0b", width=2, dash="dot"),
        ))
        _fig_comp.add_trace(_go.Scatter(
            x=_years_ax, y=_col_vals,
            name="Dólares guardados", mode="lines",
            line=dict(color="#ef4444", width=2, dash="dash"),
        ))
        _fig_comp.update_layout(
            paper_bgcolor="#0f172a",
            plot_bgcolor="#0f172a",
            font=dict(color="#94a3b8", size=12),
            xaxis=dict(
                title="Años",
                tickmode="linear", dtick=1,
                gridcolor="#1e293b", zerolinecolor="#1e293b",
            ),
            yaxis=dict(
                title=_disp_curr,
                range=[_y_min, _y_max],
                gridcolor="#1e293b", zerolinecolor="#1e293b",
                tickformat=",.0f",
            ),
            legend=dict(
                orientation="h", yanchor="bottom", y=1.02,
                xanchor="left", x=0,
                bgcolor="rgba(0,0,0,0)",
            ),
            margin=dict(l=0, r=0, t=40, b=0),
            hovermode="x unified",
        )
        st.plotly_chart(_fig_comp, use_container_width=True)
    except Exception:
        pass

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Si agregás algo todos los meses ──────────────────────────────────────
    st.markdown('<div class="section-title">💰 ¿Qué pasa si sumás un poco cada mes?</div>', unsafe_allow_html=True)
    st.caption("La riqueza no se construye de una vez — se construye mes a mes. Incluso montos pequeños hacen una diferencia enorme a largo plazo.")

    _aporte_key = "aporte_mensual_usd"
    _col_aporte, _col_slider = st.columns([1, 2])
    with _col_aporte:
        if _currency_in == "ARS":
            _aporte_label = f"Aporte mensual en ARS (≈ USD al MEP)"
            _aporte_ars   = st.number_input(
                _aporte_label, min_value=0, max_value=50_000_000,
                value=st.session_state.get(_aporte_key + "_ars", 50_000),
                step=50_000, key=_aporte_key + "_ars",
            )
            _aporte_usd_val = _aporte_ars / _MEP_RATE
        else:
            _aporte_usd_val = st.number_input(
                "Aporte mensual en USD", min_value=0, max_value=500_000,
                value=st.session_state.get(_aporte_key, 100),
                step=100, key=_aporte_key,
            )

    _proy = proyectar_con_aportes(
        _capital_usd, _aporte_usd_val, profile["horizon"], portfolio["expected_cagr"]
    )
    _proy_sin  = _proy["final_sin"]  * _disp_factor
    _proy_con  = _proy["final_con"]  * _disp_factor
    _proy_ext  = _proy["ganancia_extra"] * _disp_factor
    _total_ap  = _proy["total_aportado"] * _disp_factor

    with _col_slider:
        if _aporte_usd_val > 0:
            st.markdown(f"""<div style="padding:16px;background:rgba(34,197,94,0.08);border-radius:12px;border:1px solid rgba(34,197,94,0.2);">
<div style="font-size:0.85rem;opacity:0.7;">Aportando {_disp_prefix}{_aporte_usd_val*_disp_factor:,.0f}{_disp_suffix}/mes durante {profile['horizon']} años:</div>
<div style="font-size:1.6rem;font-weight:800;color:#22c55e;">{_disp_prefix}{_proy_con:,.0f}{_disp_suffix}</div>
<div style="font-size:0.8rem;opacity:0.6;">vs {_disp_prefix}{_proy_sin:,.0f}{_disp_suffix} sin aportar · ganancia extra: {_disp_prefix}{_proy_ext:,.0f}{_disp_suffix}</div>
</div>""", unsafe_allow_html=True)
        else:
            st.info("Ingresá un monto mensual para ver el impacto")

    if _aporte_usd_val > 0:
        try:
            import plotly.graph_objects as _go2
            _ap_años   = _proy["años"]
            _ap_con    = [v * _disp_factor for v in _proy["con_aporte"]]
            _ap_sin    = [v * _disp_factor for v in _proy["sin_aporte"]]
            _ap_y_min  = min(_ap_sin) * 0.97
            _ap_y_max  = max(_ap_con) * 1.03

            _fig_ap = _go2.Figure()
            _fig_ap.add_trace(_go2.Scatter(
                x=_ap_años, y=_ap_con,
                name=f"Con aportes mensuales", mode="lines",
                line=dict(color="#22c55e", width=3),
                fill="tonexty",
                fillcolor="rgba(34,197,94,0.08)",
            ))
            _fig_ap.add_trace(_go2.Scatter(
                x=_ap_años, y=_ap_sin,
                name="Sin aportes", mode="lines",
                line=dict(color="#60a5fa", width=2, dash="dot"),
            ))
            _fig_ap.update_layout(
                paper_bgcolor="#0f172a",
                plot_bgcolor="#0f172a",
                font=dict(color="#94a3b8", size=12),
                xaxis=dict(
                    title="Años",
                    tickmode="linear", dtick=1,
                    gridcolor="#1e293b", zerolinecolor="#1e293b",
                ),
                yaxis=dict(
                    title=_disp_curr,
                    range=[_ap_y_min, _ap_y_max],
                    gridcolor="#1e293b", zerolinecolor="#1e293b",
                    tickformat=",.0f",
                ),
                legend=dict(
                    orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0,
                    bgcolor="rgba(0,0,0,0)",
                ),
                margin=dict(l=0, r=0, t=40, b=0),
                hovermode="x unified",
            )
            st.plotly_chart(_fig_ap, use_container_width=True)
        except Exception:
            pass

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Guía de compra ────────────────────────────────────────────────────────
    render_buy_guide(portfolio)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Backtesting humanizado ────────────────────────────────────────────────
    st.markdown('<div class="section-title">⏱️ ¿Qué hubiera pasado si ya estabas invertido?</div>', unsafe_allow_html=True)
    st.caption("Usamos precios históricos reales para mostrarte cuánto hubiera cambiado tu capital.")

    _bt_days_opts = {
        "últimos 30 días": 30,
        "últimos 3 meses": 90,
        "últimos 6 meses": 180,
        "último año":      365,
    }
    _bt_label_sel = st.radio(
        "Mirá qué hubiera pasado en los",
        list(_bt_days_opts.keys()),
        index=1,
        horizontal=True,
        key="bt_period_radio",
        label_visibility="collapsed",
    )
    _bt_days_sel = _bt_days_opts[_bt_label_sel]

    # Cache estable por perfil + días seleccionados (v3 — fix MultiIndex yfinance)
    _bt_cache_key = f"_bt_human_v3_{_bt_days_sel}_{profile['risk_profile']}_{int(_capital_usd)}"
    if _bt_cache_key not in st.session_state:
        with st.spinner("Calculando..."):
            try:
                from modules.backtester import backtest_portfolio as _backtest
                st.session_state[_bt_cache_key] = _backtest(portfolio["positions"], days=_bt_days_sel)
            except Exception as _e:
                st.session_state[_bt_cache_key] = {"error": str(_e)}

    _bth = st.session_state.get(_bt_cache_key, {})

    if _bth.get("error"):
        st.caption(f"No pudimos obtener datos históricos en este momento. ({_bth['error']})")
    elif _bth.get("portfolio_return") is not None:
        _bth_pr   = _bth["portfolio_return"]          # %
        _bth_br   = _bth["benchmark_return"]
        _bth_al   = _bth["alpha"]
        # Capital en la moneda que el usuario ve
        _bth_cap_disp  = _disp_capital
        _bth_final     = _bth_cap_disp * (1 + _bth_pr / 100)
        _bth_diff      = _bth_final - _bth_cap_disp
        _bth_diff_sign = "+" if _bth_diff >= 0 else ""
        _bth_color     = "#22c55e" if _bth_pr >= 0 else "#ef4444"
        _bth_emoji     = "📈" if _bth_pr >= 0 else "📉"
        _bth_verb      = "habrías ganado" if _bth_diff >= 0 else "habrías perdido"

        # Headline
        st.markdown(f"""
<div style="background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:16px;padding:28px 32px;margin:12px 0 20px;">
  <div style="font-size:1.05rem;color:#94a3b8;margin-bottom:8px;">Si hubieras empezado en los {_bt_label_sel} con esta misma cartera...</div>
  <div style="font-size:2.4rem;font-weight:800;color:{_bth_color};line-height:1.1;">
    {_bth_emoji} {_bth_verb} {_disp_prefix}{abs(_bth_diff):,.0f}{_disp_suffix}
  </div>
  <div style="font-size:1.1rem;color:#e2e8f0;margin-top:8px;">
    Tus {_disp_prefix}{_bth_cap_disp:,.0f}{_disp_suffix} serían hoy
    <strong style="color:{_bth_color};">{_disp_prefix}{_bth_final:,.0f}{_disp_suffix}</strong>
    &nbsp;({_bth_diff_sign}{_bth_pr:.1f}%)
  </div>
</div>
""", unsafe_allow_html=True)

        # Comparación con el mercado (solo si tenemos benchmark)
        if _bth_al is not None and _bth_br is not None:
            _bth_al_color = "#22c55e" if _bth_al >= 0 else "#ef4444"
            _bth_al_text  = f"le ganó al mercado general por {abs(_bth_al):.1f} puntos" if _bth_al >= 0 else f"estuvo {abs(_bth_al):.1f} puntos por debajo del mercado general"
            st.markdown(f"""
<div style="background:#1e293b;border-radius:12px;padding:16px 24px;margin-bottom:16px;display:flex;align-items:center;gap:12px;">
  <span style="font-size:1.4rem;">🏆</span>
  <div>
    <div style="color:#94a3b8;font-size:0.85rem;">Comparado con el S&P 500 en el mismo período</div>
    <div style="color:{_bth_al_color};font-weight:600;">Esta cartera {_bth_al_text}
    (S&P 500: {("+" if _bth_br >= 0 else "")}{_bth_br:.1f}%)</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # Gráfico con tu dinero real
        _bth_cd = _bth.get("chart_data", [])
        if _bth_cd:
            import pandas as pd
            _bth_df = pd.DataFrame(_bth_cd)
            _bth_df["date"] = pd.to_datetime(_bth_df["date"])
            _bth_df = _bth_df.set_index("date")
            # Escalar a capital real del usuario
            _bth_df["portfolio"]  = _bth_cap_disp * (1 + (_bth_df["portfolio"]  - 100) / 100)
            _bth_df["benchmark"]  = _bth_cap_disp * (1 + (_bth_df["benchmark"]  - 100) / 100)
            _bth_df.columns = [f"Tu cartera ({_disp_curr})", f"S&P 500 ({_disp_curr})"]
            st.line_chart(_bth_df, use_container_width=True)

        # Activos — expander suave
        _bth_pu = _bth.get("positions_used", [])
        if _bth_pu:
            with st.expander("¿Cuál activo aportó más?"):
                for _pos in sorted(_bth_pu, key=lambda x: x["return"], reverse=True):
                    _pc = "#22c55e" if _pos["return"] >= 0 else "#ef4444"
                    _ps = "+" if _pos["return"] >= 0 else ""
                    _pm = _bth_cap_disp * _pos["weight"] * _pos["return"] / 100
                    _pms = "+" if _pm >= 0 else ""
                    st.markdown(
                        f"**{_pos['label']}** — "
                        f"<span style='color:{_pc};'>{_ps}{_pos['return']:.1f}% "
                        f"({_pms}{_disp_prefix}{abs(_pm):,.0f}{_disp_suffix})</span>",
                        unsafe_allow_html=True,
                    )

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

# ══════════════════════════════════════════════════════════════════════════════
# METODOLOGÍA
# ══════════════════════════════════════════════════════════════════════════════
elif step == "metodologia":
    render_methodology()

render_footer()
