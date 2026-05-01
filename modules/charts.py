"""
Módulo de visualizaciones
"""

import re
import math
import plotly.graph_objects as go
import streamlit as st


PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans, sans-serif", color="#94a3b8"),
    margin=dict(l=0, r=0, t=10, b=0),
)

# ── Macro-categorías para el gráfico de 2 capas ────────────────────────────────
_MACRO_MAP: dict[str, tuple[str, str]] = {
    "Pesos ARS":    ("Liquidez ARS",            "#a3e635"),
    "Dólar MEP":    ("Cobertura Cambiaria",      "#38bdf8"),
    "Bonos USD":    ("Renta Fija USD",           "#4fa3ff"),
    "CEDEARs":      ("Renta Variable Intl.",     "#a78bfa"),
    "ETFs":         ("Fondos Globales (ETFs)",   "#10d98a"),
    "Acciones ARG": ("Acciones Argentinas",      "#f59e0b"),
    "Cripto":       ("Alternativos",             "#f97316"),
}

# ── Guía de compra: plataforma + cómo buscarlo ────────────────────────────────
_PLATFORMS: dict[str, tuple[str, str]] = {
    "cash_pesos":      ("Naranja X, Ualá, Mercado Pago",    "App → sección 'Cuenta'"),
    "money_market":    ("IOL, Mercado Pago, Ualá, Balanz",  "Fondos → Money Market"),
    "plazo_fijo":      ("Tu banco (Galicia, Santander…)",   "App del banco → Inversiones"),
    "fci_t0":          ("IOL, PPI, Balanz",                 "Fondos → Renta Fija T+0"),
    "lecap":           ("IOL, PPI, Balanz",                 "Renta Fija → S31M26 / S30J26"),
    "cer_bond":        ("IOL, PPI, Balanz",                 "Renta Fija → TX26 / TX28"),
    "fci_renta_pesos": ("IOL, PPI, SBS",                   "Fondos → Renta Fija"),
    "mep":             ("IOL, PPI, Balanz, Cocos",          "Dólar MEP → operación AL30 48hs"),
    "al30":            ("IOL, PPI, Balanz, Cocos",          "Renta Fija → AL30"),
    "gd30":            ("IOL, PPI, Balanz",                 "Renta Fija → GD30"),
    "on_ypf":          ("IOL, PPI",                        "Renta Fija → YPFDS"),
    "on_corp":         ("IOL, PPI",                        "Renta Fija → PTSTO / TCCUD"),
    "on_pampa":        ("IOL, PPI",                        "Renta Fija → PTSTO"),
    "on_tecpetrol":    ("IOL, PPI",                        "Renta Fija → TCCUD"),
    "spy":             ("IOL, PPI, Balanz",                 "CEDEARs → SPY"),
    "qqq":             ("IOL, PPI, Balanz",                 "CEDEARs → QQQ"),
    "eem":             ("IOL, PPI",                        "CEDEARs → EEM"),
    "iau":             ("IOL, PPI",                        "CEDEARs → IAU"),
    "vti":             ("IOL, PPI",                        "CEDEARs → VTI"),
    "gld":             ("IOL, PPI",                        "CEDEARs → GLD"),
    "aapl":            ("IOL, PPI, Balanz",                 "CEDEARs → AAPL"),
    "msft":            ("IOL, PPI, Balanz",                 "CEDEARs → MSFT"),
    "googl":           ("IOL, PPI",                        "CEDEARs → GOOGL"),
    "amzn":            ("IOL, PPI",                        "CEDEARs → AMZN"),
    "nvda":            ("IOL, PPI, Balanz",                 "CEDEARs → NVDA"),
    "meli":            ("IOL, PPI, Balanz",                 "CEDEARs → MELI"),
    "meta":            ("IOL, PPI",                        "CEDEARs → META"),
    "brk":             ("IOL, PPI",                        "CEDEARs → BRKB"),
    "jpm":             ("IOL, PPI",                        "CEDEARs → JPM"),
    "ko":              ("IOL, PPI",                        "CEDEARs → KO"),
    "wmt":             ("IOL, PPI",                        "CEDEARs → WMT"),
    "jnj":             ("IOL, PPI",                        "CEDEARs → JNJ"),
    "pfe":             ("IOL, PPI",                        "CEDEARs → PFE"),
    "xom":             ("IOL, PPI",                        "CEDEARs → XOM"),
    "tsla":            ("IOL, PPI, Balanz",                 "CEDEARs → TSLA"),
    "bac":             ("IOL, PPI",                        "CEDEARs → BAC"),
    "dis":             ("IOL, PPI",                        "CEDEARs → DIS"),
    "ypf":             ("IOL, PPI, Balanz",                 "Acciones → YPFD"),
    "galicia":         ("IOL, PPI, Balanz",                 "Acciones → GGAL"),
    "teco2":           ("IOL, PPI",                        "Acciones → TECO2"),
    "pampa":           ("IOL, PPI, Balanz",                 "Acciones → PAMP"),
    "vist":            ("IOL, PPI",                        "Acciones → VIST"),
    "bbar":            ("IOL, PPI",                        "Acciones → BBAR"),
    "loma":            ("IOL, PPI",                        "Acciones → LOMA"),
    "btc":             ("Lemon, Buenbit, Ripio, Belo",     "Cripto → BTC"),
    "eth":             ("Lemon, Buenbit, Ripio",           "Cripto → ETH"),
    "usdt":            ("Lemon, Buenbit, Belo",            "Cripto → USDT"),
}


def _t1() -> str:
    """Color de texto primario según el tema activo."""
    return "#1e293b" if st.session_state.get("theme") == "light" else "#eef2ff"


def _t2() -> str:
    """Color de texto secundario según el tema activo."""
    return "#475569" if st.session_state.get("theme") == "light" else "#94a3b8"


def _pie_border() -> str:
    return "#f1f5f9" if st.session_state.get("theme") == "light" else "#050810"


# ─── Helpers ──────────────────────────────────────────────────────────────────

def _remove_asset(portfolio: dict, asset_id: str) -> dict:
    """Elimina un activo y renormaliza todos los pesos."""
    positions = [dict(p) for p in portfolio["positions"] if p["id"] != asset_id]
    if not positions:
        return portfolio

    total = sum(p["weight"] for p in positions)
    for p in positions:
        p["weight"] = round(p["weight"] / total, 4)

    cat_exp, sec_exp, cur_exp = {}, {}, {}
    for p in positions:
        cat_exp[p["category"]] = cat_exp.get(p["category"], 0) + p["weight"]
        sec_exp[p["sub"]]      = sec_exp.get(p["sub"], 0)      + p["weight"]
        cur_exp[p["currency"]] = cur_exp.get(p["currency"], 0) + p["weight"]

    pesos_pct = sum(p["weight"] for p in positions if p["currency"] == "ARS") * 100

    return {
        **portfolio,
        "positions":           positions,
        "expected_cagr":       round(sum(p["weight"] * p["expected_return"] for p in positions), 4),
        "expected_volatility": round(sum(p["weight"] * p["volatility"]      for p in positions), 4),
        "category_exposure":   cat_exp,
        "sector_exposure":     sec_exp,
        "currency_exposure":   cur_exp,
        "pesos_pct":           round(pesos_pct, 1),
        "usd_pct":             round(100 - pesos_pct, 1),
    }


# ─── Torta (2 capas: macro → detalle) ────────────────────────────────────────

def render_pie_chart(portfolio: dict):
    positions = portfolio["positions"]

    # Agregar por macro-categoría (Capa 1)
    macro_data: dict = {}
    for p in positions:
        macro_name, macro_color = _MACRO_MAP.get(p["category"], (p["category"], "#94a3b8"))
        if macro_name not in macro_data:
            macro_data[macro_name] = {"weight": 0.0, "color": macro_color, "assets": []}
        macro_data[macro_name]["weight"] += p["weight"]
        macro_data[macro_name]["assets"].append(p)

    sorted_macro = sorted(macro_data.items(), key=lambda x: -x[1]["weight"])

    labels = [m[0] for m in sorted_macro]
    values = [round(m[1]["weight"] * 100, 1) for m in sorted_macro]
    colors = [m[1]["color"] for m in sorted_macro]

    hovers = []
    for name, info in sorted_macro:
        lines = "<br>".join(
            f"  · {a['name'].split('(')[0].split('—')[0].strip()} ({a['weight']*100:.0f}%)"
            for a in sorted(info["assets"], key=lambda x: -x["weight"])
        )
        hovers.append(f"<b>{name}</b> — {info['weight']*100:.0f}%<br>{lines}")

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.52,
        marker=dict(colors=colors, line=dict(color=_pie_border(), width=2)),
        hovertemplate="%{customdata}<extra></extra>",
        customdata=hovers,
        textfont=dict(size=11, color=_t1()),
        textinfo="percent",
        showlegend=True,
    )])

    fig.update_layout(
        **PLOTLY_LAYOUT,
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=10, color=_t2()),
            bgcolor="rgba(0,0,0,0)",
        ),
        annotations=[dict(
            text=f"<b>{portfolio['risk_profile'].upper()}</b>",
            x=0.5, y=0.5,
            font=dict(size=13, color=_t1(), family="Syne, sans-serif"),
            showarrow=False,
        )],
        height=380,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Capa 2: desglose por macro-categoría
    with st.expander("Ver desglose detallado →"):
        for name, info in sorted_macro:
            pct = info["weight"] * 100
            color = info["color"]
            st.markdown(
                f'<div class="macro-cat-header" style="border-left-color:{color};">'
                f'<span class="macro-cat-name">{name}</span>'
                f'<span class="macro-cat-pct">{pct:.0f}%</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            for a in sorted(info["assets"], key=lambda x: -x["weight"]):
                a_pct = a["weight"] * 100
                st.markdown(
                    f'<div class="macro-asset-row">'
                    f'<span class="macro-asset-dot" style="background:{a["color"]};"></span>'
                    f'<span class="macro-asset-name">{a["name"].split("(")[0].split("—")[0].strip()}</span>'
                    f'<span class="macro-asset-ticker">{a["ticker"]}</span>'
                    f'<span class="macro-asset-pct">{a_pct:.1f}%</span>'
                    f'</div>',
                    unsafe_allow_html=True,
                )


# ─── Gráfico de evolución (3 líneas simples) ──────────────────────────────────

def render_evolution_chart(simulation: dict, initial_capital: float, years: int):
    t    = simulation["years_axis"]
    sc   = simulation["scenarios"]
    summ = simulation["summary"]

    fig = go.Figure()

    # Pésimo
    fig.add_trace(go.Scatter(
        x=t, y=sc["pesimista"],
        mode="lines",
        name="😟 Pésimo",
        line=dict(color="#ef4444", width=2.5, dash="dot"),
        hovertemplate="Año %{x:.0f}: $%{y:,.0f}<extra>Pésimo</extra>",
    ))

    # Base
    fig.add_trace(go.Scatter(
        x=t, y=sc["base"],
        mode="lines",
        name="📊 Base",
        line=dict(color="#f0b429", width=3),
        hovertemplate="Año %{x:.0f}: $%{y:,.0f}<extra>Base</extra>",
    ))

    # Excelente
    fig.add_trace(go.Scatter(
        x=t, y=sc["optimista"],
        mode="lines",
        name="🚀 Excelente",
        line=dict(color="#10d98a", width=2.5, dash="dot"),
        hovertemplate="Año %{x:.0f}: $%{y:,.0f}<extra>Excelente</extra>",
    ))

    fig.add_hline(
        y=initial_capital,
        line_dash="dot",
        line_color="rgba(100,116,139,0.4)",
        line_width=1,
        annotation_text=f"Capital inicial: ${initial_capital:,.0f}",
        annotation_font=dict(size=10, color="#64748b"),
    )

    fig.update_layout(
        **PLOTLY_LAYOUT,
        xaxis=dict(
            title="Años",
            showgrid=True,
            gridcolor="rgba(99,120,180,0.07)",
            zeroline=False,
            tickfont=dict(size=10),
        ),
        yaxis=dict(
            title="Valor USD",
            showgrid=True,
            gridcolor="rgba(99,120,180,0.07)",
            zeroline=False,
            tickformat="$,.0f",
            tickfont=dict(size=10),
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.14,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        hovermode="x unified",
        height=360,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Solo 2 métricas, con lenguaje simple
    col1, col2 = st.columns(2)
    with col1:
        prob_g = summ["prob_positive"] * 100
        st.markdown(f"""<div class="metric-card" style="text-align:center;">
<div class="metric-label">Chances de ganar plata</div>
<div class="metric-value" style="color:#22c55e;">{prob_g:.0f}%</div>
<div class="metric-sub">De terminar con más de lo que pusiste</div>
</div>""", unsafe_allow_html=True)
    with col2:
        prob_d = summ["prob_double"] * 100
        st.markdown(f"""<div class="metric-card" style="text-align:center;">
<div class="metric-label">Chances de duplicar</div>
<div class="metric-value" style="color:#60a5fa;">{prob_d:.0f}%</div>
<div class="metric-sub">De terminar con el doble o más</div>
</div>""", unsafe_allow_html=True)


# ─── Gráfico de barras: proyección a 1, 5 y 10 años ──────────────────────────

def render_bar_simulation(portfolio: dict, initial_capital: float,
                          currency: str = "USD", capital_original: float = None):
    cagr = portfolio["expected_cagr"]
    vol  = portfolio["expected_volatility"]

    cagr_opt  = cagr + vol * 0.5
    cagr_pess = max(cagr - vol * 0.7, -0.30)

    years  = [1, 5, 10]
    labels = ["1 año", "5 años", "10 años"]

    # factor de conversión para mostrar en la moneda del usuario
    if capital_original is None:
        capital_original = initial_capital
    display_factor = capital_original / initial_capital if initial_capital else 1.0

    def proj(c, y):    return initial_capital * math.exp(c * y)
    def proj_d(c, y):  return proj(c, y) * display_factor
    def pct(v):        return (v / initial_capital - 1) * 100

    vals_pess = [proj(cagr_pess, y) for y in years]
    vals_base = [proj(cagr,      y) for y in years]
    vals_opt  = [proj(cagr_opt,  y) for y in years]

    # valores escalados a la moneda del usuario para display
    disp_pess = [proj_d(cagr_pess, y) for y in years]
    disp_base = [proj_d(cagr,      y) for y in years]
    disp_opt  = [proj_d(cagr_opt,  y) for y in years]

    currency_label = "ARS" if currency == "ARS" else "USD"
    currency_note  = (
        "Los montos están expresados en pesos argentinos (ARS)"
        if currency == "ARS"
        else "Los montos están expresados en dólares (USD)"
    )

    def fmt(v):     return f"${v:,.0f}"
    def fmt_pct(v):
        p    = pct(v)
        sign = "+" if p >= 0 else ""
        return f"{sign}{p:.0f}%"

    fig = go.Figure()

    # Pésimo
    fig.add_trace(go.Bar(
        name="😟 Pésimo",
        x=labels,
        y=disp_pess,
        marker_color="#ef4444",
        marker_line_width=0,
        opacity=0.85,
        text=[f"{fmt(d)}<br><span style='font-size:11px'>{fmt_pct(v)}</span>" for d, v in zip(disp_pess, vals_pess)],
        textposition="outside",
        textfont=dict(size=11, color="#ef4444"),
        hovertemplate=f"<b>%{{x}} — Pésimo</b><br>Capital: $%{{y:,.0f}} {currency_label}<extra></extra>",
    ))

    # Base
    fig.add_trace(go.Bar(
        name="📊 Base",
        x=labels,
        y=disp_base,
        marker_color="#f0b429",
        marker_line_width=0,
        opacity=0.9,
        text=[f"{fmt(d)}<br><span style='font-size:11px'>{fmt_pct(v)}</span>" for d, v in zip(disp_base, vals_base)],
        textposition="outside",
        textfont=dict(size=11, color="#f0b429"),
        hovertemplate=f"<b>%{{x}} — Base</b><br>Capital: $%{{y:,.0f}} {currency_label}<extra></extra>",
    ))

    # Optimista
    fig.add_trace(go.Bar(
        name="🚀 Excelente",
        x=labels,
        y=disp_opt,
        marker_color="#10d98a",
        marker_line_width=0,
        opacity=0.9,
        text=[f"{fmt(d)}<br><span style='font-size:11px'>{fmt_pct(v)}</span>" for d, v in zip(disp_opt, vals_opt)],
        textposition="outside",
        textfont=dict(size=11, color="#10d98a"),
        hovertemplate=f"<b>%{{x}} — Excelente</b><br>Capital: $%{{y:,.0f}} {currency_label}<extra></extra>",
    ))

    # Línea de capital inicial
    fig.add_hline(
        y=capital_original,
        line_dash="dot",
        line_color="rgba(148,163,184,0.4)",
        line_width=1.5,
        annotation_text=f"Capital inicial ${capital_original:,.0f}",
        annotation_position="top left",
        annotation_font=dict(size=10, color="#64748b"),
    )

    fig.update_layout(
        **PLOTLY_LAYOUT,
        barmode="group",
        bargap=0.22,
        bargroupgap=0.06,
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(99,120,180,0.07)",
            zeroline=False,
            tickformat="$,.0f",
            tickfont=dict(size=10),
            title="",
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=13, family="Space Grotesk, sans-serif", color=_t1()),
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.12,
            xanchor="center",
            x=0.5,
            font=dict(size=11),
            bgcolor="rgba(0,0,0,0)",
        ),
        height=420,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        f'<p class="chart-currency-note">{currency_note}</p>',
        unsafe_allow_html=True,
    )

    # Métricas clave debajo
    col1, col2, col3 = st.columns(3)
    gain_1_d  = disp_base[0] - capital_original
    gain_10_d = disp_base[2] - capital_original

    with col1:
        st.markdown(f"""<div class="metric-card" style="text-align:center;">
<div class="metric-label">Ganancia en 1 año (base)</div>
<div class="metric-value" style="color:#f0b429;">+${gain_1_d:,.0f}</div>
<div class="metric-sub">Escenario más probable</div>
</div>""", unsafe_allow_html=True)
    with col2:
        gain_10_pct = pct(vals_base[2])
        st.markdown(f"""<div class="metric-card" style="text-align:center;">
<div class="metric-label">Ganancia en 10 años (base)</div>
<div class="metric-value" style="color:#10d98a;">+{gain_10_pct:.0f}%</div>
<div class="metric-sub">${gain_10_d:,.0f} sobre lo invertido</div>
</div>""", unsafe_allow_html=True)
    with col3:
        worst     = vals_pess[2]
        worst_d   = disp_pess[2]
        worst_pct = pct(worst)
        color = "#22c55e" if worst_pct >= 0 else "#ef4444"
        sign  = "+" if worst_pct >= 0 else ""
        st.markdown(f"""<div class="metric-card" style="text-align:center;">
<div class="metric-label">Peor escenario a 10 años</div>
<div class="metric-value" style="color:{color};">{sign}{worst_pct:.0f}%</div>
<div class="metric-sub">${worst_d:,.0f} en el peor caso</div>
</div>""", unsafe_allow_html=True)


# ─── Tabla de activos con botón de eliminar ───────────────────────────────────

def render_allocation_table(portfolio: dict, capital: float, currency_label: str = "USD"):
    positions  = portfolio["positions"]
    can_remove = len(positions) > 2

    if "show_detail_table" not in st.session_state:
        st.session_state.show_detail_table = False
    if "pending_remove_id" not in st.session_state:
        st.session_state.pending_remove_id   = None
        st.session_state.pending_remove_name = None

    # ── Vista simple (por defecto) ─────────────────────────────────────────────
    if not st.session_state.show_detail_table:
        for p in positions[:3]:
            pct       = p["weight"] * 100
            desc      = p.get("simple_desc") or p.get("description", "")[:90]
            st.markdown(
                f'<div class="asset-simple-card">'
                f'<span class="asc-dot" style="background:{p["color"]};"></span>'
                f'<div class="asc-content">'
                f'<div class="asc-name">{p["name"]}</div>'
                f'<div class="asc-desc">{desc}</div>'
                f'</div>'
                f'<div class="asc-pct">{pct:.0f}%'
                f'<span class="asc-pct-sub">de tu plata</span></div>'
                f'</div>',
                unsafe_allow_html=True,
            )

        remaining = len(positions) - 3
        extra     = f" ({remaining} más)" if remaining > 0 else ""
        if st.button(f"Ver todos los activos{extra} →", key="toggle_detail_on", use_container_width=True):
            st.session_state.show_detail_table = True
            st.rerun()
        return

    # ── Vista detallada ────────────────────────────────────────────────────────
    if st.button("↑ Ver resumen", key="toggle_detail_off"):
        st.session_state.show_detail_table = False
        st.session_state.pending_remove_id   = None
        st.session_state.pending_remove_name = None
        st.rerun()

    # Panel de confirmación de eliminación
    if st.session_state.pending_remove_id:
        pname = st.session_state.pending_remove_name
        st.markdown(
            f'<div class="remove-confirm">'
            f'¿Querés sacar <strong>{pname}</strong> de tu cartera? '
            f'Podés agregarlo de nuevo después.'
            f'</div>',
            unsafe_allow_html=True,
        )
        col_yes, col_no, _ = st.columns([1, 1, 4])
        with col_yes:
            if st.button("Sí, sacarlo", key="confirm_remove", type="primary"):
                updated = _remove_asset(portfolio, st.session_state.pending_remove_id)
                st.session_state.portfolio         = updated
                st.session_state.pending_remove_id   = None
                st.session_state.pending_remove_name = None
                st.rerun()
        with col_no:
            if st.button("Cancelar", key="cancel_remove"):
                st.session_state.pending_remove_id   = None
                st.session_state.pending_remove_name = None
                st.rerun()

    liq_colors = {
        "alta":  ("#064e3b", "#34d399"),
        "media": ("#1e3a5f", "#60a5fa"),
        "baja":  ("#7c2d12", "#fb923c"),
    }

    # Header
    h = st.columns([2.8, 1.2, 1.5, 1.4, 3.0, 1.0, 0.55])
    for col, label in zip(h, ["Instrumento", "Categoría", "Ponderación", "Importe Sugerido", "¿Para qué sirve?", "Liquidez", ""]):
        col.markdown(f'<div class="tbl-header">{label}</div>', unsafe_allow_html=True)

    st.markdown('<div class="tbl-divider"></div>', unsafe_allow_html=True)

    for p in positions:
        pct    = p["weight"] * 100
        amount = p["weight"] * capital
        liq    = p.get("liquidity", "media")
        lbg, lfg = liq_colors.get(liq, ("#1a2235", "#94a3b8"))

        bar_html = (
            f'<div class="pct-bar-bg" style="margin-top:5px;">'
            f'<div class="pct-bar-fill" style="width:{pct:.1f}%;background:{p["color"]};"></div>'
            f'</div>'
        )

        cols = st.columns([2.8, 1.2, 1.5, 1.4, 3.0, 1.0, 0.55])
        desc = p.get("simple_desc") or p.get("description", "")[:90]

        cols[0].markdown(
            f'<div class="tbl-cell">'
            f'<span class="asset-dot" style="background:{p["color"]};"></span>'
            f'<span class="asset-name">{p["name"]}</span><br>'
            f'<span class="asset-sub">{p["ticker"]} · {p["market"]}</span>'
            f'</div>',
            unsafe_allow_html=True,
        )
        cols[1].markdown(
            f'<div class="tbl-cell"><span class="tbl-text">{p["category"]}</span></div>',
            unsafe_allow_html=True,
        )
        cols[2].markdown(
            f'<div class="tbl-cell"><strong style="color:#eef2ff;">{pct:.1f}%</strong>{bar_html}</div>',
            unsafe_allow_html=True,
        )
        _amt_prefix = "$" if currency_label == "ARS" else "USD "
        cols[3].markdown(
            f'<div class="tbl-cell"><strong style="color:#eef2ff;">{_amt_prefix}{amount:,.0f}</strong></div>',
            unsafe_allow_html=True,
        )
        cols[4].markdown(
            f'<div class="tbl-cell" style="font-size:0.82rem;color:#94a3b8;line-height:1.4;">{desc}</div>',
            unsafe_allow_html=True,
        )
        cols[5].markdown(
            f'<div class="tbl-cell"><span class="tag" style="background:{lbg};color:{lfg};">{liq}</span></div>',
            unsafe_allow_html=True,
        )

        with cols[6]:
            st.markdown('<div style="padding-top:6px;">', unsafe_allow_html=True)
            if can_remove:
                is_pending = st.session_state.pending_remove_id == p["id"]
                btn_style  = "primary" if is_pending else "secondary"
                if st.button("✕", key=f"rm_{p['id']}", help="Sacar de mi cartera", type=btn_style):
                    st.session_state.pending_remove_id   = p["id"]
                    st.session_state.pending_remove_name = p["name"]
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

    # Fila de total
    _tot_prefix = "$" if currency_label == "ARS" else "USD "
    st.markdown('<div class="tbl-divider" style="margin-top:4px;"></div>', unsafe_allow_html=True)
    t_cols = st.columns([2.8, 1.2, 1.5, 1.4, 3.0, 1.0, 0.55])
    t_cols[0].markdown('<div class="tbl-cell"><strong style="color:#eef2ff;">TOTAL</strong></div>', unsafe_allow_html=True)
    t_cols[2].markdown('<div class="tbl-cell"><strong style="color:#eef2ff;">100%</strong></div>', unsafe_allow_html=True)
    t_cols[3].markdown(f'<div class="tbl-cell"><strong style="color:#eef2ff;">{_tot_prefix}{capital:,.0f}</strong></div>', unsafe_allow_html=True)
    t_cols[4].markdown(f'<div class="tbl-cell" style="font-size:0.82rem;color:#64748b;">Retorno prom. anual: <strong style="color:#10d98a;">{portfolio["expected_cagr"]*100:.1f}%</strong></div>', unsafe_allow_html=True)

    # Exposición por categoría y moneda
    st.markdown("<br>", unsafe_allow_html=True)
    col_cat, col_cur = st.columns(2)

    with col_cat:
        st.markdown("**Distribución por tipo de activo**")
        for cat, w in sorted(portfolio["category_exposure"].items(), key=lambda x: -x[1]):
            pct = w * 100
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;font-size:0.82rem;color:#94a3b8;margin-bottom:0.25rem;">'
                f'<span>{cat}</span><span style="color:#eef2ff;">{pct:.1f}%</span></div>'
                f'<div class="pct-bar-bg" style="margin-bottom:0.55rem;">'
                f'<div class="pct-bar-fill" style="width:{pct}%;background:#4fa3ff;"></div></div>',
                unsafe_allow_html=True,
            )

    with col_cur:
        st.markdown("**En pesos vs dólares**")
        cur_colors = {"USD": "#10d98a", "ARS": "#f0b429", "ARS/USD": "#60a5fa"}
        for cur, w in sorted(portfolio["currency_exposure"].items(), key=lambda x: -x[1]):
            pct = w * 100
            col = cur_colors.get(cur, "#94a3b8")
            label = {"USD": "Dólares (USD)", "ARS": "Pesos (ARS)", "ARS/USD": "Mix ARS/USD"}.get(cur, cur)
            st.markdown(
                f'<div style="display:flex;justify-content:space-between;font-size:0.82rem;color:#94a3b8;margin-bottom:0.25rem;">'
                f'<span>{label}</span><span style="color:#eef2ff;">{pct:.1f}%</span></div>'
                f'<div class="pct-bar-bg" style="margin-bottom:0.55rem;">'
                f'<div class="pct-bar-fill" style="width:{pct}%;background:{col};"></div></div>',
                unsafe_allow_html=True,
            )


# ─── Guía de compra rápida (Feature 5) ────────────────────────────────────────

def render_buy_guide(portfolio: dict):
    """Tabla compacta: ticker + plataforma para cada activo de la cartera."""
    positions = portfolio["positions"]

    with st.expander("🛒 ¿Dónde y cómo comprar cada activo?"):
        # Header
        h = st.columns([2.6, 1.1, 2.8, 2.5])
        for col, label in zip(h, ["Instrumento", "Ticker", "Plataformas", "Cómo buscarlo"]):
            col.markdown(f'<div class="tbl-header">{label}</div>', unsafe_allow_html=True)
        st.markdown('<div class="tbl-divider"></div>', unsafe_allow_html=True)

        for p in positions:
            plat, how = _PLATFORMS.get(p["id"], ("IOL, PPI", f"Buscar → {p['ticker']}"))
            short_name = p["name"].split("(")[0].split("—")[0].strip()
            if len(short_name) > 36:
                short_name = short_name[:35] + "…"

            cols = st.columns([2.6, 1.1, 2.8, 2.5])
            cols[0].markdown(
                f'<div class="tbl-cell">'
                f'<span class="asset-dot" style="background:{p["color"]};"></span>'
                f'<span class="asset-name" style="font-size:0.84rem;">{short_name}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            cols[1].markdown(
                f'<div class="tbl-cell">'
                f'<span class="buy-ticker">{p["ticker"]}</span>'
                f'</div>',
                unsafe_allow_html=True,
            )
            cols[2].markdown(
                f'<div class="tbl-cell" style="font-size:0.82rem;color:#94a3b8;">{plat}</div>',
                unsafe_allow_html=True,
            )
            cols[3].markdown(
                f'<div class="tbl-cell" style="font-size:0.8rem;color:#64748b;">{how}</div>',
                unsafe_allow_html=True,
            )

        st.markdown(
            '<p style="font-size:0.72rem;color:#64748b;margin-top:0.75rem;">'
            'IOL = InvertirOnline · PPI = Portfolio Personal Inversiones · Cocos = Cocos Capital. '
            'Verificá disponibilidad y costos operativos en cada plataforma antes de operar.'
            '</p>',
            unsafe_allow_html=True,
        )
