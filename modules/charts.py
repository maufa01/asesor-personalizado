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


# ─── Torta ────────────────────────────────────────────────────────────────────

def render_pie_chart(portfolio: dict):
    positions = portfolio["positions"]

    labels = [p["name"].split("(")[0].split("—")[0].strip() for p in positions]
    values = [round(p["weight"] * 100, 1) for p in positions]
    colors = [p["color"] for p in positions]
    hovers = [
        f"<b>{p['name']}</b><br>"
        f"Categoría: {p['category']}<br>"
        f"Peso: {p['weight']*100:.1f}%<br>"
        f"Retorno esperado: {p['expected_return']*100:.1f}%<br>"
        f"Mercado: {p['market']}"
        for p in positions
    ]

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=0.52,
        marker=dict(colors=colors, line=dict(color="#050810", width=2)),
        hovertemplate="%{customdata}<extra></extra>",
        customdata=hovers,
        textfont=dict(size=11, color="#eef2ff"),
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
            font=dict(size=10, color="#94a3b8"),
            bgcolor="rgba(0,0,0,0)",
        ),
        annotations=[dict(
            text=f"<b>{portfolio['risk_profile'].upper()}</b>",
            x=0.5, y=0.5,
            font=dict(size=13, color="#eef2ff", family="Syne, sans-serif"),
            showarrow=False,
        )],
        height=380,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


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

def render_bar_simulation(portfolio: dict, initial_capital: float):
    cagr = portfolio["expected_cagr"]
    vol  = portfolio["expected_volatility"]

    cagr_opt  = cagr + vol * 0.5
    cagr_pess = max(cagr - vol * 0.7, -0.30)

    years     = [1, 5, 10]
    labels    = ["1 año", "5 años", "10 años"]

    def proj(c, y): return initial_capital * math.exp(c * y)
    def pct(v):     return (v / initial_capital - 1) * 100

    vals_pess = [proj(cagr_pess, y) for y in years]
    vals_base = [proj(cagr,      y) for y in years]
    vals_opt  = [proj(cagr_opt,  y) for y in years]

    def fmt(v): return f"${v:,.0f}"
    def fmt_pct(v):
        p = pct(v)
        sign = "+" if p >= 0 else ""
        return f"{sign}{p:.0f}%"

    fig = go.Figure()

    # Pésimo
    fig.add_trace(go.Bar(
        name="😟 Pésimo",
        x=labels,
        y=vals_pess,
        marker_color="#ef4444",
        marker_line_width=0,
        opacity=0.85,
        text=[f"{fmt(v)}<br><span style='font-size:11px'>{fmt_pct(v)}</span>" for v in vals_pess],
        textposition="outside",
        textfont=dict(size=11, color="#ef4444"),
        hovertemplate="<b>%{x} — Pésimo</b><br>Capital: %{y:$,.0f}<extra></extra>",
    ))

    # Base
    fig.add_trace(go.Bar(
        name="📊 Base",
        x=labels,
        y=vals_base,
        marker_color="#f0b429",
        marker_line_width=0,
        opacity=0.9,
        text=[f"{fmt(v)}<br><span style='font-size:11px'>{fmt_pct(v)}</span>" for v in vals_base],
        textposition="outside",
        textfont=dict(size=11, color="#f0b429"),
        hovertemplate="<b>%{x} — Base</b><br>Capital: %{y:$,.0f}<extra></extra>",
    ))

    # Optimista
    fig.add_trace(go.Bar(
        name="🚀 Excelente",
        x=labels,
        y=vals_opt,
        marker_color="#10d98a",
        marker_line_width=0,
        opacity=0.9,
        text=[f"{fmt(v)}<br><span style='font-size:11px'>{fmt_pct(v)}</span>" for v in vals_opt],
        textposition="outside",
        textfont=dict(size=11, color="#10d98a"),
        hovertemplate="<b>%{x} — Excelente</b><br>Capital: %{y:$,.0f}<extra></extra>",
    ))

    # Línea de capital inicial
    fig.add_hline(
        y=initial_capital,
        line_dash="dot",
        line_color="rgba(148,163,184,0.4)",
        line_width=1.5,
        annotation_text=f"Capital inicial ${initial_capital:,.0f}",
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
            tickfont=dict(size=13, family="Space Grotesk, sans-serif", color="#eef2ff"),
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
        margin=dict(l=0, r=0, t=40, b=0),
        height=420,
        uniformtext=dict(minsize=9, mode="hide"),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # Métricas clave debajo
    col1, col2, col3 = st.columns(3)
    gain_1  = vals_base[0] - initial_capital
    gain_10 = vals_base[2] - initial_capital

    with col1:
        st.markdown(f"""<div class="metric-card" style="text-align:center;">
<div class="metric-label">Ganancia en 1 año (base)</div>
<div class="metric-value" style="color:#f0b429;">+${gain_1:,.0f}</div>
<div class="metric-sub">Escenario más probable</div>
</div>""", unsafe_allow_html=True)
    with col2:
        gain_10_pct = pct(vals_base[2])
        st.markdown(f"""<div class="metric-card" style="text-align:center;">
<div class="metric-label">Ganancia en 10 años (base)</div>
<div class="metric-value" style="color:#10d98a;">+{gain_10_pct:.0f}%</div>
<div class="metric-sub">${gain_10:,.0f} sobre lo invertido</div>
</div>""", unsafe_allow_html=True)
    with col3:
        worst = vals_pess[2]
        worst_pct = pct(worst)
        color = "#22c55e" if worst_pct >= 0 else "#ef4444"
        sign  = "+" if worst_pct >= 0 else ""
        st.markdown(f"""<div class="metric-card" style="text-align:center;">
<div class="metric-label">Peor escenario a 10 años</div>
<div class="metric-value" style="color:{color};">{sign}{worst_pct:.0f}%</div>
<div class="metric-sub">${worst:,.0f} en el peor caso</div>
</div>""", unsafe_allow_html=True)


# ─── Tabla de activos con botón de eliminar ───────────────────────────────────

def render_allocation_table(portfolio: dict, capital: float):
    positions = portfolio["positions"]
    can_remove = len(positions) > 2

    tag_bg = {
        "mínimo":     ("#064e3b", "#34d399"),
        "muy bajo":   ("#1e3a5f", "#60a5fa"),
        "bajo":       ("#14532d", "#86efac"),
        "bajo-medio": ("#365314", "#bef264"),
        "medio":      ("#713f12", "#fcd34d"),
        "medio-alto": ("#7c2d12", "#fb923c"),
        "alto":       ("#7f1d1d", "#f87171"),
    }

    # Header
    h = st.columns([3.2, 1.4, 1.8, 1.4, 1.2, 1.3, 0.55])
    for col, label in zip(h, ["Activo", "Categoría", "Peso", "Monto (USD)", "Retorno", "Riesgo", ""]):
        col.markdown(f'<div class="tbl-header">{label}</div>', unsafe_allow_html=True)

    st.markdown('<div class="tbl-divider"></div>', unsafe_allow_html=True)

    to_remove = None
    for p in positions:
        pct    = p["weight"] * 100
        amount = p["weight"] * capital
        risk   = p["risk_level"]
        bg, fg = tag_bg.get(risk, ("#1a2235", "#94a3b8"))

        bar_html = (
            f'<div class="pct-bar-bg" style="margin-top:5px;">'
            f'<div class="pct-bar-fill" style="width:{pct:.1f}%;background:{p["color"]};"></div>'
            f'</div>'
        )

        cols = st.columns([3.2, 1.4, 1.8, 1.4, 1.2, 1.3, 0.55])

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
        cols[3].markdown(
            f'<div class="tbl-cell"><strong style="color:#eef2ff;">${amount:,.0f}</strong></div>',
            unsafe_allow_html=True,
        )
        cols[4].markdown(
            f'<div class="tbl-cell" style="color:#10d98a;">{p["expected_return"]*100:.1f}%</div>',
            unsafe_allow_html=True,
        )
        cols[5].markdown(
            f'<div class="tbl-cell"><span class="tag" style="background:{bg};color:{fg};">{risk}</span></div>',
            unsafe_allow_html=True,
        )

        with cols[6]:
            st.markdown('<div style="padding-top:6px;">', unsafe_allow_html=True)
            if can_remove:
                if st.button("✕", key=f"rm_{p['id']}", help=f"Quitar {p['name']}"):
                    to_remove = p["id"]
            st.markdown('</div>', unsafe_allow_html=True)

    # Fila de total
    st.markdown('<div class="tbl-divider" style="margin-top:4px;"></div>', unsafe_allow_html=True)
    t_cols = st.columns([3.2, 1.4, 1.8, 1.4, 1.2, 1.3, 0.55])
    t_cols[0].markdown('<div class="tbl-cell"><strong style="color:#eef2ff;">TOTAL</strong></div>', unsafe_allow_html=True)
    t_cols[2].markdown('<div class="tbl-cell"><strong style="color:#eef2ff;">100%</strong></div>', unsafe_allow_html=True)
    t_cols[3].markdown(f'<div class="tbl-cell"><strong style="color:#eef2ff;">${capital:,.0f}</strong></div>', unsafe_allow_html=True)
    t_cols[4].markdown(f'<div class="tbl-cell"><strong style="color:#10d98a;">{portfolio["expected_cagr"]*100:.1f}%</strong></div>', unsafe_allow_html=True)

    # Procesar eliminación
    if to_remove:
        updated = _remove_asset(portfolio, to_remove)
        st.session_state.portfolio = updated
        st.rerun()

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
