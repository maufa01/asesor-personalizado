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

_CATEGORY_ORDER = [
    "Liquidez",
    "Cobertura cambiaria",
    "Renta fija",
    "Fondos globales",
    "Renta variable",
]

_CATEGORY_META = {
    "Liquidez": {
        "icon":        "💵",
        "description": "Plata disponible en todo momento. La podés retirar cuando quieras, sin esperar ni pagar penalidades.",
        "color":       "#60a5fa",
    },
    "Cobertura cambiaria": {
        "icon":        "🛡️",
        "description": "Dólares legales comprados por la bolsa. Protege sus ahorros de la devaluación del peso.",
        "color":       "#f59e0b",
    },
    "Renta fija": {
        "icon":        "📄",
        "description": "Préstamos a empresas o al Estado que le devuelven su dinero con intereses en dólares. Más predecible que las acciones.",
        "color":       "#22c55e",
    },
    "Fondos globales": {
        "icon":        "🌍",
        "description": "Acciones de las 500 empresas más grandes del mundo: Apple, Google, Amazon y más. Todo en una sola compra.",
        "color":       "#4fa3ff",
    },
    "Renta variable": {
        "icon":        "📈",
        "description": "Acciones con mayor potencial de crecimiento a largo plazo. El precio puede subir y bajar más que el resto.",
        "color":       "#a78bfa",
    },
}

_CATEGORY_ASSET_IDS = {
    "Liquidez": {"cash_pesos", "money_market", "plazo_fijo", "fci_t0"},
    "Cobertura cambiaria": {"mep"},
    "Renta fija": {"lecap", "cer_bond", "fci_renta_pesos", "al30", "gd30", "on_ypf", "on_corp", "on_pampa", "on_tecpetrol"},
    "Fondos globales": {"spy", "qqq", "vti"},
    "Renta variable": {"aapl", "msft", "nvda", "meli", "ypf", "galicia"},
}

# ── Macro-categorías para el gráfico de 2 capas ────────────────────────────────
_MACRO_MAP = {
    "Pesos ARS":    ("Liquidez ARS",            "#a3e635"),
    "Dólar MEP":    ("Cobertura Cambiaria",      "#38bdf8"),
    "Bonos USD":    ("Renta Fija USD",           "#4fa3ff"),
    "CEDEARs":      ("Renta Variable Intl.",     "#a78bfa"),
    "ETFs":         ("Fondos Globales (ETFs)",   "#10d98a"),
    "Acciones ARG": ("Acciones Argentinas",      "#f59e0b"),
}

# ── Guía de compra: plataforma + cómo buscarlo ────────────────────────────────
_PLATFORMS = {
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


# ─── Torta (misma categorización que la tabla de instrumentos) ───────────────

def render_pie_chart(portfolio: dict):
    positions = portfolio["positions"]

    # Usar la misma lógica que render_allocation_table para que ambas vistas sean consistentes
    cat_data: dict = {}
    for p in positions:
        cat   = _asset_to_user_category(p)
        color = _CATEGORY_META.get(cat, {}).get("color", "#94a3b8")
        if cat not in cat_data:
            cat_data[cat] = {"weight": 0.0, "color": color, "assets": []}
        cat_data[cat]["weight"] += p["weight"]
        cat_data[cat]["assets"].append(p)

    # Ordenar según _CATEGORY_ORDER para que sea consistente con la tabla
    sorted_macro = sorted(
        cat_data.items(),
        key=lambda x: (_CATEGORY_ORDER.index(x[0]) if x[0] in _CATEGORY_ORDER else 99),
    )

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

    # Capa 2: desglose (mismas categorías que la tabla de abajo)
    with st.expander("Ver desglose detallado →"):
        for name, info in sorted_macro:
            pct   = info["weight"] * 100
            color = info["color"]
            icon  = _CATEGORY_META.get(name, {}).get("icon", "📊")
            st.markdown(
                f'<div class="macro-cat-header" style="border-left-color:{color};">'
                f'<span class="macro-cat-name">{icon}&nbsp;{name}</span>'
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

def _asset_to_user_category(asset: dict) -> str:
    aid = asset.get("id", "")
    if aid in _CATEGORY_ASSET_IDS["Liquidez"]:
        return "Liquidez"
    if aid in _CATEGORY_ASSET_IDS["Cobertura cambiaria"]:
        return "Cobertura cambiaria"
    if aid in _CATEGORY_ASSET_IDS["Fondos globales"]:
        return "Fondos globales"
    if aid in _CATEGORY_ASSET_IDS["Renta fija"]:
        return "Renta fija"
    if aid in _CATEGORY_ASSET_IDS["Renta variable"]:
        return "Renta variable"
    if asset.get("category") in {"CEDEARs", "Acciones ARG", "Acciones"}:
        return "Renta variable"
    if asset.get("category") in {"Bonos USD", "Dólar MEP", "Pesos ARS"}:
        return "Renta fija"
    return "Renta variable"


def _group_positions_by_user_category(positions: list) -> dict:
    groups = {cat: [] for cat in _CATEGORY_ORDER}
    for p in positions:
        category = _asset_to_user_category(p)
        groups.setdefault(category, []).append(p)
    return groups


def render_allocation_table(portfolio: dict, capital: float, currency_label: str = "USD"):
    """
    Nivel 1: cards de categorías siempre visibles (sin siglas).
    Nivel 2: expander por categoría con los activos específicos.
    """
    positions  = portfolio["positions"]
    groups     = _group_positions_by_user_category(positions)
    amt_prefix = "$" if currency_label == "ARS" else "USD "

    for category in _CATEGORY_ORDER:
        items = groups.get(category, [])
        if not items:
            continue

        pct   = sum(p["weight"] for p in items) * 100
        meta  = _CATEGORY_META[category]
        icon  = meta["icon"]
        color = meta["color"]

        # ── Nivel 1: card de categoría (siempre visible) ──────────────────
        st.markdown(
            f'<div class="cat-l1-card" style="border-left-color:{color};">'
            f'  <div class="cat-l1-body">'
            f'    <div class="cat-l1-name">{icon}&nbsp; {category}</div>'
            f'    <div class="cat-l1-desc">{meta["description"]}</div>'
            f'  </div>'
            f'  <div class="cat-l1-right">'
            f'    <div class="cat-l1-pct" style="color:{color};">{pct:.0f}%</div>'
            f'    <div class="cat-l1-pct-sub">de su dinero</div>'
            f'  </div>'
            f'</div>',
            unsafe_allow_html=True,
        )

        # ── Nivel 2: activos específicos (expandible) ─────────────────────
        n     = len(items)
        label = f"Ver {'los ' if n > 1 else 'el '}{n} activo{'s' if n > 1 else ''} que componen esta categoría"
        with st.expander(label, expanded=False):
            for p in items:
                a_pct = p["weight"] * 100
                a_amt = p["weight"] * capital
                desc  = p.get("simple_desc") or p.get("description", "")
                ticker = p.get("ticker", "")
                plat, _ = _PLATFORMS.get(p["id"], ("IOL, PPI", ""))
                short_name = p["name"].split("(")[0].split("—")[0].strip()
                st.markdown(
                    f'<div class="asset-detail-card" style="border-left-color:{p["color"]};">'
                    f'  <div class="adc-top">'
                    f'    <div class="adc-title-wrap">'
                    f'      <div class="adc-title">{short_name}</div>'
                    f'      <div class="adc-meta">{ticker} · {plat}</div>'
                    f'    </div>'
                    f'    <div class="adc-right">'
                    f'      <div class="adc-pct">{a_pct:.0f}%</div>'
                    f'      <div class="adc-amt">{amt_prefix}{a_amt:,.0f}</div>'
                    f'    </div>'
                    f'  </div>'
                    f'  <div class="adc-desc">{desc}</div>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        st.markdown('<div style="height:0.4rem;"></div>', unsafe_allow_html=True)


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
