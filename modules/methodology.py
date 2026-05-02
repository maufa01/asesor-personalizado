"""
Página de metodología: explica el framework académico del sistema.
Para presentación institucional (rector, docentes, inversores).
"""

import streamlit as st


def render_methodology():
    st.markdown('<div class="section-title">🎓 Metodología del Sistema</div>', unsafe_allow_html=True)
    st.caption("Fundamentos teóricos y técnicos del motor de construcción de carteras.")

    # ── Tabs principales ──────────────────────────────────────────────────────
    tabs = st.tabs([
        "📐 Framework general",
        "🔢 Scoring de activos",
        "🏗️ Construcción del portafolio",
        "📡 Señales de mercado",
        "🧠 Sistema de aprendizaje",
        "📊 Fuentes de datos",
    ])

    # ── Tab 1: Framework general ──────────────────────────────────────────────
    with tabs[0]:
        st.markdown("""
### Arquitectura del sistema

El sistema sigue un pipeline de 6 etapas que transforma las respuestas del inversor
en una cartera personalizada con fundamentos cuantitativos:
""")
        st.markdown("""
| Etapa | Componente | Descripción |
|---|---|---|
| 1 | **Perfil de riesgo** | 8 preguntas → 4 perfiles (Conservador / Estable / Moderado / Agresivo) |
| 2 | **Scoring de activos** | 75 tickers evaluados en 5 bloques fundamentales (0–100 pts) |
| 3 | **Selección por buckets** | Cada perfil tiene segmentos con candidatos rankeados por score |
| 4 | **Ajustes dinámicos** | Horizonte, fondo de emergencia, experiencia, ingresos |
| 5 | **Señales de sector** | Histórico de valuación sectorial ajusta pesos ±15% |
| 6 | **Filtros estructurales** | Liquidez mínima, overlap ETF/acciones, concentración |
""")

        st.markdown("---")
        st.markdown("""
### Teoría de base

El sistema integra conceptos de **Modern Portfolio Theory (Markowitz, 1952)**
con ajustes para el mercado argentino:

- **Diversificación**: el índice HHI (Herfindahl-Hirschman) mide la concentración de la cartera.
  HHI < 0.15 indica alta diversificación.
- **Riesgo-retorno**: el Sharpe Ratio cuantifica el exceso de retorno por unidad de riesgo
  asumida, usando el T-Bill de EE.UU. como tasa libre de riesgo (≈ 4.5% anual).
- **Beta de portfolio**: mide la sensibilidad de la cartera al mercado. Beta = 1 implica
  movimiento idéntico al mercado; < 1 implica menor volatilidad sistemática.
- **Ajuste por perfil**: los pesos no son fijos — emergen del scoring de cada activo
  candidato dentro de cada segmento (bucket), ponderados proporcionalmente a su score.
""")

    # ── Tab 2: Scoring de activos ─────────────────────────────────────────────
    with tabs[1]:
        st.markdown("""
### Framework de scoring: 5 bloques (0–100 puntos)

Cada activo equity se evalúa en 5 dimensiones con **umbrales diferenciados por sector**.
Los bonos tienen su propio framework de 5 bloques (Rendimiento / Duración / Calidad / Paridad / Liquidez).
""")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
**Bloque 1 — Valuación (25 pts)**
- Forward P/E vs umbrales sectoriales (7 pts)
- EV/EBITDA (8 pts)
- PEG ratio (5 pts)
- Dividend Yield (5 pts)

**Bloque 2 — Calidad (25 pts)**
- ROE vs umbrales por sector (10 pts)
- Margen neto (8 pts)
- ROA (7 pts)

**Bloque 3 — Solvencia (20 pts)**
- Deuda/Equity — no aplica para bancos (10 pts)
- Current ratio (5 pts)
- Quick ratio (5 pts)
""")
        with col2:
            st.markdown("""
**Bloque 4 — Crecimiento (20 pts)**
- EPS CAGR 5 años (8 pts)
- Ventas CAGR 5 años (7 pts)
- EPS trimestral Q/Q (5 pts)

**Bloque 5 — Cualitativo (10 pts)**
- Recomendación de analistas: escala 1–5 (4 pts)
  - ≤ 2.0 = Strong Buy → 4 pts
  - ≤ 2.5 = Buy → 3 pts
- Upside al precio objetivo consenso (3 pts)
  - > 15% upside → 3 pts
- Short float < 2% → señal de confianza (3 pts)

**Ajuste ARG** — descuento regulatorio adicional para acciones argentinas:
riesgo país, liquidez BYMA, exposición cambiaria.
""")

        st.markdown("---")
        st.markdown("""
### Umbrales sectoriales

Los umbrales **no son universales** — cada sector tiene sus propios parámetros.
Ejemplo: un P/E de 25× es "excelente" en tecnología pero "neutral" en energía.
""")
        st.markdown("""
| Sector | Forward P/E excelente | ROE excelente | EV/EBITDA excelente |
|---|---|---|---|
| Tecnología | ≤ 18× | ≥ 25% | ≤ 15× |
| Bancos | ≤ 8× | ≥ 18% | N/A |
| Energía | ≤ 7× | ≥ 15% | ≤ 5× |
| Consumo defensivo | ≤ 16× | ≥ 20% | ≤ 12× |
| Salud | ≤ 14× | ≥ 20% | ≤ 12× |
| Utilities | ≤ 12× | ≥ 12% | ≤ 8× |
| Industriales | ≤ 13× | ≥ 20% | ≤ 10× |
""")

        st.markdown("""
### Rating final

| Score | Rating | Acción |
|---|---|---|
| 85–100 | **STRONG BUY** | Incluir con peso máximo |
| 70–84 | **BUY** | Incluir con peso estándar |
| 55–69 | **HOLD** | Incluir si el perfil lo permite |
| 40–54 | **UNDERWEIGHT** | Solo en perfiles agresivos |
| 0–39 | **AVOID** | No incluir en ningún perfil |
""")

    # ── Tab 3: Construcción del portafolio ────────────────────────────────────
    with tabs[2]:
        st.markdown("""
### Sistema de buckets por perfil

Cada perfil de riesgo tiene segmentos predefinidos con target de peso y candidatos.
El algoritmo selecciona los mejores activos **por score** dentro de cada segmento:
""")
        st.markdown("""
| Perfil | Buckets principales |
|---|---|
| **Conservador** | Liquidez ARS · Cobertura MEP · Renta fija USD · ETF global |
| **Estable** | Liquidez · MEP · Renta fija · ETF global · 1 acción ARG |
| **Moderado** | MEP · Renta fija · ETF global · Equity global · Equity ARG |
| **Agresivo** | MEP · Renta fija mínima · ETF tech · Equity global × 3 · Equity ARG × 2 |
""")

        st.markdown("---")
        st.markdown("""
### Ponderación score-driven

Dentro de cada bucket, los pesos son **proporcionales al score**:

```
weight_i = score_i / Σ score_j   (para todos j en el bucket)
```

Esto significa que un activo con score 80 recibe el doble de peso
que uno con score 40, dentro del mismo segmento. No hay pesos arbitrarios.

### Ajustes secuenciales

Sobre la asignación base se aplican ajustes en cascada:

1. **Horizonte temporal**: > 10 años → reduce liquidez, sube equity
2. **Fondo de emergencia**: si no tiene → sube liquidez 10%
3. **Experiencia**: principiante → reemplaza acciones individuales por ETFs
4. **Ingresos**: irregulares → sube liquidez, reduce volátiles 25%
5. **Señales de sector**: sobrepondera sectores baratos vs su historia
6. **Filtros**: liquidez mínima, exclusión de overlaps ETF/stocks
""")

    # ── Tab 4: Señales de mercado ─────────────────────────────────────────────
    with tabs[3]:
        st.markdown("""
### Señal de valuación sectorial

El sistema acumula medianas históricas de cada sector cada vez que corre el scorer.
Con ≥ 5 snapshots históricos, calcula una señal compuesta:

```
signal = 0.60 × score_signal + 0.40 × pe_signal

score_signal = (score_actual - score_histórico_promedio) / score_histórico_promedio
pe_signal    = (pe_histórico_promedio - pe_actual) / pe_histórico_promedio
```

**Interpretación:**
- Signal > 0 → sector más atractivo que su historia → sobrepesar hasta +15%
- Signal < 0 → sector más caro que su historia → subpesar hasta -15%
- |Signal| > 0.30 → clampeado a ±0.30 (evita sobreajuste)

### Ajuste de memoria individual

Si el sistema detecta que una acción perdió > 5% desde la última evaluación:
aplica -5 puntos al score en la próxima cartera.

Si ganó > 10%: aplica +3 puntos. Clampeado a [-20, +10].

Esto evita que el sistema siga recomendando activos que demostraron mal desempeño.
""")

    # ── Tab 5: Sistema de aprendizaje ────────────────────────────────────────
    with tabs[4]:
        st.markdown("""
### Memoria del sistema

El sistema mantiene un archivo `memory.json` con tres niveles de aprendizaje:
""")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
**Nivel 1: Historial de carteras**
- Cada cartera generada queda registrada con fecha, composición y perfil
- Permite detectar patrones de rendimiento entre sesiones
- Base para las señales de ajuste individual
""")
        with col2:
            st.markdown("""
**Nivel 2: Medianas de sector**
- Snapshots periódicos de PE, EV/EBITDA y score por sector
- Se acumulan para construir la serie histórica
- Alimentan las señales de valuación sectorial
""")
        with col3:
            st.markdown("""
**Nivel 3: Ajustes por ticker**
- Registro de retornos observados por activo
- Ajuste dinámico de score individual
- Sesgos de mercado local detectados automáticamente
""")

        st.markdown("---")
        st.info("El sistema de aprendizaje es incremental: en las primeras semanas, las señales de sector son neutras. A medida que acumula snapshots, las señales se vuelven estadísticamente confiables.")

    # ── Tab 6: Fuentes de datos ───────────────────────────────────────────────
    with tabs[5]:
        st.markdown("""
### Fuentes de datos del sistema
""")
        st.markdown("""
| Dato | Fuente | Frecuencia | Método |
|---|---|---|---|
| Fundamentals equity (PE, ROE, márgenes, etc.) | **Finviz.com** | Semanal | Web scraping via finvizfinance |
| Precios y volumen de bonos ARG | **Rava.com** | Por corrida | API JSON + HTML fallback |
| TIR estimada de bonos | **BOND_DEFS estáticos** | Manual | Actualizable en código |
| Tipo de cambio MEP | **dolarapi.com** | Tiempo real (cache 30 min) | REST API pública |
| Precios históricos para backtesting | **Yahoo Finance** | Por consulta | yfinance |
| Recomendación de analistas | **Finviz.com** | Semanal | Campo "Recom." del screener |
| Precio objetivo consenso | **Finviz.com** | Semanal | Campo "Target Price" |
| Scores de bonos ARG | **bond_scorer.py** | Por corrida | Motor propio |
""")

        st.markdown("---")
        st.markdown("""
### Universo de activos cubierto

- **75 tickers** scrapeados de Finviz (CEDEARs + ADRs argentinos)
- **13 bonos** en `BOND_DEFS` (soberanos USD, LECAPs, ONs corporativas)
- **3 sectores con benchmarks**: utilities (5 tickers), materiales (5), transporte (5)
  → garantizan señales de sector con mínimo 5 puntos de datos
- **6 ETFs globales**: SPY, QQQ, VTI, IAU, GLD, EEM
- **Activos en pesos**: plazo fijo, money market, FCI T+0, FCI renta fija
""")

        st.markdown("""
### Limitaciones conocidas

- La TIR de bonos ARG es mayormente estática (no hay API oficial confiable con datos de TIR en tiempo real)
- La memoria es local al entorno de deployment (no persiste entre instancias de Streamlit Cloud)
- El backtesting cubre solo la porción equity (bonos y pesos sin series históricas en Yahoo Finance)
- Los scores se actualizan semanalmente, no en tiempo real
""")

        if st.button("← Volver a la cartera", key="back_from_methodology"):
            st.session_state.step = st.session_state.get("_prev_step", "results")
            st.rerun()
