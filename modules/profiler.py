"""
Cuestionario de perfil de inversor — rediseñado para principiantes reales.
Lenguaje cotidiano, situaciones concretas, sin tecnicismos.
"""

import streamlit as st


QUESTIONS = [
    {
        "id": "motivation",
        "emoji": "🤔",
        "step": "1 de 8",
        "title": "¿Qué te trajo acá hoy?",
        "hint": "Elegí la que más se parece a tu situación real.",
        "options": [
            ("La inflación me come los ahorros. Quiero al menos no perder valor.", 0),
            ("Tengo plata quieta y quiero que me genere algo, sin complicarme.", 1),
            ("Quiero hacer crecer mi plata a mediano plazo. Entiendo que hay riesgos.", 2),
            ("Busco la mayor rentabilidad posible. Estoy dispuesto a asumir riesgos.", 3),
        ],
    },
    {
        "id": "loss_reaction",
        "emoji": "📉",
        "step": "2 de 8",
        "title": "Invertís $500.000 hoy. Al mes siguiente ves en la app que valen $430.000. ¿Qué hacés?",
        "hint": "Estas caídas son normales en ciertos tipos de inversión. Sé honesto con vos mismo.",
        "options": [
            ("Los saco de inmediato. No puedo ver eso.", 0),
            ("Saco la mitad para no perder más.", 1),
            ("No hago nada. Entiendo que puede pasar y espero.", 2),
            ("Meto más plata. Si bajó, está más barato.", 3),
        ],
    },
    {
        "id": "horizon",
        "emoji": "📅",
        "step": "3 de 8",
        "title": "¿Para cuándo vas a necesitar esa plata?",
        "hint": "Pensá en tus planes reales: viaje, auto, casa, jubilación...",
        "options": [
            ("La puedo necesitar en cualquier momento. Menos de un año.", 0),
            ("En 1 a 3 años. Tengo algo planificado.", 1),
            ("En 3 a 7 años. Estoy construyendo algo a futuro.", 2),
            ("No la voy a tocar en mucho tiempo. Es para el largo plazo.", 3),
        ],
    },
    {
        "id": "income_stability",
        "emoji": "💼",
        "step": "4 de 8",
        "title": "¿Cómo son tus ingresos mes a mes?",
        "hint": "Esto es clave para saber si podés aguantar un mal momento sin tener que rescatar tu inversión.",
        "options": [
            ("Irregulares o sin ingreso fijo. Nunca sé cuánto voy a cobrar.", 0),
            ("Varían bastante. Dependo de ventas, clientes o proyectos.", 1),
            ("Tengo sueldo fijo o algo estable y predecible.", 2),
            ("Muy estables. Tengo varias fuentes de ingresos.", 3),
        ],
    },
    {
        "id": "emergency_fund",
        "emoji": "🛡️",
        "step": "5 de 8",
        "title": "Si mañana se te rompe el auto o tenés un gasto inesperado grande, ¿podés cubrirlo sin tocar esta inversión?",
        "hint": "Tener un fondo de emergencia es la base de cualquier inversión sana.",
        "options": [
            ("No. No tengo nada extra guardado.", 0),
            ("Tengo algo, pero alcanzaría para 1 o 2 meses.", 1),
            ("Tengo entre 3 y 6 meses de gastos guardados.", 2),
            ("Sí. Tengo más de 6 meses cubiertos cómodamente.", 3),
        ],
    },
    {
        "id": "risk_appetite",
        "emoji": "🎲",
        "step": "6 de 8",
        "title": "Si tuvieras que elegir, ¿con cuál te quedás?",
        "hint": "No hay respuesta correcta. Pensá cómo te sentirías realmente en cada caso.",
        "options": [
            ("Ganar siempre un 5% fijo al año. Sin sorpresas, sin emociones.", 0),
            ("Poder ganar 15%, aunque algún año pueda perder 5%.", 1),
            ("Poder ganar 30%, aunque algún año pueda perder 20%.", 2),
            ("Poder ganar 60%, aunque algún año pueda perder 40%.", 3),
        ],
    },
    {
        "id": "experience",
        "emoji": "📚",
        "step": "7 de 8",
        "title": "¿Cuánto sabés de inversiones hoy?",
        "hint": "Sé honesto, no hay respuesta mala. Sirve para adaptar lo que te recomendamos.",
        "options": [
            ("Prácticamente nada. Nunca invertí en mi vida.", 0),
            ("Solo conozco el plazo fijo o Mercado Pago.", 1),
            ("Algo. Escuché de CEDEARs, fondos, dólar MEP.", 2),
            ("Bastante. Ya operé acciones, bonos o cripto.", 3),
        ],
    },
    {
        "id": "mindset",
        "emoji": "🧠",
        "step": "8 de 8",
        "title": "¿Con cuál de estas frases te identificás más?",
        "hint": "La última pregunta. Elegí la que más resuena con tu forma de pensar.",
        "options": [
            ("Prefiero mil veces dormir tranquilo que ganar más.", 0),
            ("Busco un equilibrio. Seguridad con algo de crecimiento.", 1),
            ("Me importa el resultado a largo plazo más que las caídas de corto.", 2),
            ("Estoy enfocado en maximizar mi patrimonio. El riesgo es parte del juego.", 3),
        ],
    },
]

HORIZON_MAP = {
    "La puedo necesitar en cualquier momento. Menos de un año.": 1,
    "En 1 a 3 años. Tengo algo planificado.": 2,
    "En 3 a 7 años. Estoy construyendo algo a futuro.": 5,
    "No la voy a tocar en mucho tiempo. Es para el largo plazo.": 10,
}

PROFILES = {
    "conservador": {
        "emoji": "🟢",
        "label": "Inversor Conservador",
        "color": "#22c55e",
        "tagline": "Tu prioridad es la seguridad. Y eso está muy bien.",
        "explanation": (
            "Preferís dormir tranquilo antes que apostar por grandes ganancias. "
            "No estás dispuesto a ver caídas fuertes y eso es completamente válido — "
            "especialmente si recién arrancás o si necesitás el dinero en el corto plazo. "
            "Una cartera conservadora no es \"para los que no saben\": "
            "es para los que tienen claras sus prioridades."
        ),
        "what_means": [
            "📦 La mayor parte de tu plata va a activos muy seguros",
            "💵 Protección contra la inflación y la devaluación del peso",
            "🔒 Poca volatilidad — tu saldo no va a oscilar mucho",
            "📈 Rendimiento moderado, consistente y predecible",
        ],
        "first_steps": [
            "Empezá con un Fondo Money Market en IOL o Mercado Pago (retiro en el día)",
            "Comprá Dólar MEP para dolarizar una parte de tus ahorros",
            "Mirá bonos CER (TX26) para protegerte de la inflación en pesos",
        ],
    },
    "moderado": {
        "emoji": "🟡",
        "label": "Inversor Moderado",
        "color": "#f59e0b",
        "tagline": "Buscás un equilibrio inteligente.",
        "explanation": (
            "Querés que tu plata crezca, pero sin pegarte un susto enorme. "
            "Estás dispuesto a tolerar alguna baja temporal si eso significa "
            "mejores resultados a mediano plazo. "
            "Es el perfil más común y, para muchas personas, el más inteligente: "
            "combina protección con crecimiento real."
        ),
        "what_means": [
            "⚖️ Mezcla de activos seguros y activos de crecimiento",
            "🌎 Diversificación entre pesos, dólares y activos internacionales",
            "📊 Rendimiento superior al plazo fijo con riesgo controlado",
            "📉 Puede haber meses negativos, pero el largo plazo es positivo",
        ],
        "first_steps": [
            "Una base en fondos conservadores (money market + bonos) para la liquidez",
            "CEDEARs del S&P500 (SPY) para exposición al mercado americano en pesos",
            "Algo de bonos en dólares (ONs corporativas) para renta en USD",
        ],
    },
    "estable": {
        "emoji": "🔵",
        "label": "Inversor Estable",
        "color": "#60a5fa",
        "tagline": "Algo mejor que un plazo fijo, sin complicaciones.",
        "explanation": (
            "Querés que tu plata trabaje más que un plazo fijo "
            "pero sin exponerte a grandes caídas. "
            "Es el punto intermedio perfecto: más rendimiento que la caja de ahorro "
            "sin los altibajos del mercado de acciones. "
            "Ideal para quien empieza a diversificar y quiere dormir tranquilo."
        ),
        "what_means": [
            "💵 Mayoría en dólares y bonos de empresas sólidas",
            "📈 Rendimiento esperado superior al plazo fijo tradicional",
            "🛡️ Poca volatilidad — tu saldo no varía mucho mes a mes",
            "🌎 Algo de exposición al mercado global para algo de crecimiento",
        ],
        "first_steps": [
            "Comprá Dólar MEP en IOL o PPI — 1 click, sin límite mensual",
            "Invertí en ONs corporativas como las de Pampa Energía o MercadoLibre",
            "Comprá el CEDEAR del S&P 500 (SPY) para algo de crecimiento en pesos",
        ],
    },
    "agresivo": {
        "emoji": "🔴",
        "label": "Inversor Agresivo",
        "color": "#ef4444",
        "tagline": "Jugás en modo largo plazo y a fondo.",
        "explanation": (
            "Tenés claro que para ganar más hay que asumir más riesgo. "
            "Estás dispuesto a ver caídas fuertes sin desesperarte, "
            "porque tu horizonte es largo y tu objetivo es maximizar el crecimiento. "
            "Importante: esto no significa tirar la plata — significa invertir "
            "con estrategia en activos de alto potencial."
        ),
        "what_means": [
            "🚀 Alta exposición a acciones argentinas e internacionales",
            "⚡ Mayor volatilidad — podés ver caídas de 20-30% sin que sea una señal de vender",
            "💎 Potencial de rendimiento muy superior al largo plazo",
            "🧩 Incluye tecnología global, mercados emergentes y algo de cripto",
        ],
        "first_steps": [
            "CEDEARs de tecnología: Nvidia, Meta, Amazon, MercadoLibre",
            "ETF QQQ o SPY para exposición amplia al mercado americano",
            "Acciones argentinas: YPF, Galicia, Vista Energy para apuesta local",
        ],
    },
}


def _score_to_profile(score: int, max_score: int) -> str:
    ratio = score / max_score
    if ratio < 0.26:       # 0-6 pts: quiere solo seguridad
        return "conservador"
    elif ratio < 0.46:     # 7-11 pts: algo mejor que plazo fijo pero sin sustos
        return "estable"
    elif ratio < 0.68:     # 12-16 pts: equilibrio crecimiento/seguridad
        return "moderado"
    else:                  # 17-24 pts: maximizar crecimiento
        return "agresivo"


def render_profiler() -> dict | None:
    answers     = st.session_state.get("answers", {})
    q_ids       = [q["id"] for q in QUESTIONS]
    answered    = len([k for k in answers if k in q_ids])
    has_capital = "capital" in answers
    has_reveal  = answers.get("_reveal_done", False)
    total_steps = len(QUESTIONS) + 1  # preguntas + capital

    # ── Barra de progreso ──────────────────────────────────────────────────────
    if not has_reveal:
        progress_pct = int(min((answered + (1 if has_capital else 0)) / total_steps, 1.0) * 100)
        st.markdown(f"""<div class="progress-wrap">
<div class="progress-label">Tu progreso</div>
<div class="progress-track"><div class="progress-fill" style="width:{progress_pct}%"></div></div>
</div>""", unsafe_allow_html=True)

    # ── Preguntas del cuestionario ─────────────────────────────────────────────
    if answered < len(QUESTIONS):
        q = QUESTIONS[answered]

        st.markdown(f"""<div class="profiler-card">
<div class="q-emoji">{q['emoji']}</div>
<h3 class="q-title">{q['title']}</h3>
<p class="hint">{q['hint']}</p>
</div>""", unsafe_allow_html=True)

        col_q, _ = st.columns([2, 1])
        with col_q:
            option_labels = [o[0] for o in q["options"]]
            selected = st.radio(
                label="Opción",
                options=option_labels,
                key=f"radio_{q['id']}",
                label_visibility="collapsed",
            )

            col_b1, col_b2 = st.columns([1, 2])
            with col_b1:
                if answered > 0 and st.button("← Atrás", key=f"back_{q['id']}"):
                    prev_id = QUESTIONS[answered - 1]["id"]
                    answers.pop(prev_id, None)
                    st.session_state.answers = answers
                    st.rerun()
            with col_b2:
                label = "Siguiente →" if answered < len(QUESTIONS) - 1 else "Última pregunta →"
                if st.button(label, key=f"next_{q['id']}", use_container_width=True):
                    answers[q["id"]] = selected
                    st.session_state.answers = answers
                    st.rerun()

        return None

    # ── Pregunta de capital ────────────────────────────────────────────────────
    if not has_capital:
        st.markdown("""<div class="profiler-card">
<div class="q-emoji">💵</div>
<h3 class="q-title">¿Con cuánta plata querés empezar?</h3>
<p class="hint">No hay mínimo perfecto. Con poco también se puede invertir bien. Podés cambiar esto después.</p>
</div>""", unsafe_allow_html=True)

        col_q, _ = st.columns([2, 1])
        with col_q:
            currency_choice = st.radio(
                "Moneda",
                ["Pesos argentinos (ARS)", "Dólares (USD)"],
                key="currency_choice",
                horizontal=True,
            )

            if "Pesos" in currency_choice:
                amount_ars = st.number_input(
                    "Monto en pesos",
                    min_value=10_000,
                    max_value=500_000_000,
                    value=500_000,
                    step=10_000,
                    format="%d",
                    key="capital_ars",
                    label_visibility="collapsed",
                )
                st.caption(f"💵 Aproximadamente USD {amount_ars / 1100:,.0f} al tipo de cambio MEP (~$1.100/USD)")
                capital_usd      = amount_ars / 1100
                capital_display  = f"${amount_ars:,.0f} ARS"
                currency         = "ARS"
                capital_original = float(amount_ars)
            else:
                capital_usd = st.number_input(
                    "Monto en USD",
                    min_value=100,
                    max_value=10_000_000,
                    value=5_000,
                    step=100,
                    key="capital_usd_input",
                    label_visibility="collapsed",
                )
                st.caption(f"💵 USD {capital_usd:,.0f}")
                capital_display  = f"USD {capital_usd:,.0f}"
                currency         = "USD"
                capital_original = float(capital_usd)

            col_b1, col_b2 = st.columns([1, 2])
            with col_b1:
                if st.button("← Atrás", key="back_capital"):
                    prev_id = QUESTIONS[-1]["id"]
                    answers.pop(prev_id, None)
                    st.session_state.answers = answers
                    st.rerun()
            with col_b2:
                if st.button("🎯 Ver mi perfil de inversor", key="finish_btn", use_container_width=True):
                    answers["capital"]          = float(capital_usd)
                    answers["capital_display"]  = capital_display
                    answers["currency"]         = currency
                    answers["capital_original"] = capital_original
                    st.session_state.answers    = answers
                    st.rerun()

        return None

    # ── Calcular perfil ────────────────────────────────────────────────────────
    total_score = 0
    max_score   = len(QUESTIONS) * 3

    for q in QUESTIONS:
        raw_val   = answers.get(q["id"])
        score_val = next((s for lbl, s in q["options"] if lbl == raw_val), 0)
        total_score += score_val

    risk_profile = _score_to_profile(total_score, max_score)
    p            = PROFILES[risk_profile]

    # ── Pantalla de reveal del perfil ──────────────────────────────────────────
    if not has_reveal:
        pct_score = int((total_score / max_score) * 100)

        st.markdown(f"""<div class="reveal-card">
<div class="reveal-badge" style="border-color:{p['color']};color:{p['color']};">
  {p['emoji']} {p['label']}
</div>
<p class="reveal-tagline">{p['tagline']}</p>
<p class="reveal-explanation">{p['explanation']}</p>
</div>""", unsafe_allow_html=True)

        what_means_html  = "".join(f'<div class="reveal-item">{item}</div>' for item in p['what_means'])
        first_steps_html = "".join(f'<div class="reveal-item">✅ {step}</div>' for step in p['first_steps'])
        st.markdown(f"""<div class="reveal-columns">
<div class="reveal-section">
<div class="reveal-section-title">📋 Lo que esto significa para tu cartera</div>
{what_means_html}
</div>
<div class="reveal-section">
<div class="reveal-section-title">🚀 Por dónde empezar</div>
{first_steps_html}
</div>
</div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        _, col_cta, _ = st.columns([1, 2, 1])
        with col_cta:
            if st.button("📊 Ver mi cartera personalizada →", key="to_portfolio", use_container_width=True):
                answers["_reveal_done"] = True
                st.session_state.answers = answers
                st.rerun()
        return None

    # ── Devolver perfil al app principal ──────────────────────────────────────
    horizon_label = answers.get("horizon", "En 3 a 7 años. Estoy construyendo algo a futuro.")
    horizon_years = HORIZON_MAP.get(horizon_label, 5)
    capital       = answers.get("capital", 5_000.0)
    p_data        = PROFILES[risk_profile]

    return {
        "risk_profile":       risk_profile,
        "risk_score":         total_score,
        "risk_max":           max_score,
        "horizon":            horizon_years,
        "capital":            capital,
        "capital_display":    answers.get("capital_display", f"USD {capital:,.0f}"),
        "currency":           answers.get("currency", "USD"),
        "capital_original":   answers.get("capital_original", capital),
        "income_stability":   answers.get("income_stability", ""),
        "loss_tolerance":     answers.get("loss_reaction", ""),
        "objective":          answers.get("motivation", ""),
        "experience":         answers.get("experience", ""),
        "emergency_fund":     answers.get("emergency_fund", ""),
        "profile_label":      p_data["label"],
        "profile_tagline":    p_data["tagline"],
        "profile_explanation":p_data["explanation"],
        "raw_answers":        answers,
    }
