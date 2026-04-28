"""
Cuestionario de perfil de inversor — lenguaje simple para principiantes argentinos
"""

import streamlit as st


QUESTIONS = [
    {
        "id": "objective",
        "emoji": "🎯",
        "title": "¿Para qué querés invertir tu plata?",
        "hint": "Elegí la opción que más se parezca a lo que buscás.",
        "type": "radio",
        "options": [
            ("Cuidarla y que no pierda valor por la inflación", 0),
            ("Que me genere un ingreso extra cada mes o año", 1),
            ("Que crezca a un ritmo razonable sin muchos sustos", 2),
            ("Que crezca lo más posible, aunque haya momentos difíciles", 3),
        ],
    },
    {
        "id": "horizon",
        "emoji": "📅",
        "title": "¿Cuándo pensás necesitar ese dinero?",
        "hint": "No hay respuesta incorrecta. Es para saber cuánto tiempo tenés para invertir.",
        "type": "radio",
        "options": [
            ("En menos de 1 año", 0),
            ("En 1 a 3 años", 1),
            ("En 3 a 7 años", 2),
            ("En más de 7 años (o no lo sé)", 3),
        ],
    },
    {
        "id": "loss_tolerance",
        "emoji": "📉",
        "title": "Imaginá que invertís $100.000 y en 3 meses ves que valen $80.000. ¿Qué hacés?",
        "hint": "Estas caídas son normales en algunos tipos de inversión.",
        "type": "radio",
        "options": [
            ("Saco todo. No aguanto ver que pierdo plata", 0),
            ("Saco una parte para no perder más", 1),
            ("No hago nada y espero que se recupere", 2),
            ("Aprovecho y pongo más plata, está más barato", 3),
        ],
    },
    {
        "id": "income_stability",
        "emoji": "💰",
        "title": "¿Cómo son tus ingresos?",
        "hint": "Esto ayuda a saber si podés aguantar una mala racha sin tocas tus inversiones.",
        "type": "radio",
        "options": [
            ("Son muy irregulares o no tengo ingresos fijos", 0),
            ("Varían bastante, dependen de lo que vendo o cobro", 1),
            ("Tengo sueldo fijo o algo parecido", 2),
            ("Tengo ingresos muy estables, incluso de varias fuentes", 3),
        ],
    },
    {
        "id": "experience",
        "emoji": "📚",
        "title": "¿Ya invertiste antes?",
        "hint": "Sé honesto, no hay respuesta mala. Sirve para adaptar la recomendación.",
        "type": "radio",
        "options": [
            ("Nunca. Soy nuevo en esto", 0),
            ("Solo plazo fijo o Mercado Pago", 1),
            ("Algo de fondos, CEDEARs o bonos", 2),
            ("Opero seguido: acciones, cripto, derivados", 3),
        ],
    },
    {
        "id": "emergency_fund",
        "emoji": "🛡️",
        "title": "¿Tenés plata guardada para emergencias (aparte de lo que querés invertir)?",
        "hint": "Es importante tener un colchón antes de invertir. Sin eso, puede que necesites rescatar antes de tiempo.",
        "type": "radio",
        "options": [
            ("No, no tengo nada guardado", 0),
            ("Tengo para menos de 3 meses de gastos", 1),
            ("Tengo para 3 a 6 meses de gastos", 2),
            ("Sí, tengo más de 6 meses cubiertos", 3),
        ],
    },
]

HORIZON_MAP = {
    "En menos de 1 año": 1,
    "En 1 a 3 años": 2,
    "En 3 a 7 años": 5,
    "En más de 7 años (o no lo sé)": 10,
}


def _score_to_profile(score: int, max_score: int) -> str:
    ratio = score / max_score
    if ratio < 0.38:
        return "conservador"
    elif ratio < 0.68:
        return "moderado"
    else:
        return "agresivo"


def render_profiler() -> dict | None:
    answers   = st.session_state.get("answers", {})
    total_q   = len(QUESTIONS) + 1
    answered  = len([k for k in answers if k in [q["id"] for q in QUESTIONS]])
    has_capital = "capital" in answers

    # ── Barra de progreso ──────────────────────────────────────────────────────
    progress = (answered + (1 if has_capital else 0)) / total_q
    st.progress(progress)
    st.caption(f"Pregunta {min(answered + 1, total_q)} de {total_q}")

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
                if answered > 0 and st.button("← Anterior", key=f"back_{q['id']}"):
                    prev_id = QUESTIONS[answered - 1]["id"]
                    answers.pop(prev_id, None)
                    st.session_state.answers = answers
                    st.rerun()
            with col_b2:
                if st.button("Siguiente →", key=f"next_{q['id']}", use_container_width=True):
                    answers[q["id"]] = selected
                    st.session_state.answers = answers
                    st.rerun()

        return None

    # ── Pregunta de capital ────────────────────────────────────────────────────
    if not has_capital:
        st.markdown("""<div class="profiler-card">
<div class="q-emoji">💵</div>
<h3 class="q-title">¿Cuánto dinero querés invertir?</h3>
<p class="hint">Podés usar pesos argentinos o dólares. Ingresá el monto que tenés disponible.</p>
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
                capital_usd = amount_ars / 1100
                capital_display = f"${amount_ars:,.0f} ARS"
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
                capital_display = f"USD {capital_usd:,.0f}"

            col_b1, col_b2 = st.columns([1, 2])
            with col_b1:
                if st.button("← Anterior", key="back_capital"):
                    prev_id = QUESTIONS[-1]["id"]
                    answers.pop(prev_id, None)
                    st.session_state.answers = answers
                    st.rerun()
            with col_b2:
                if st.button("🎯 Ver mi cartera recomendada", key="finish_btn", use_container_width=True):
                    answers["capital"]         = float(capital_usd)
                    answers["capital_display"] = capital_display
                    st.session_state.answers   = answers
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
    horizon_label = answers.get("horizon", "En 3 a 7 años")
    horizon_years = HORIZON_MAP.get(horizon_label, 5)
    capital       = answers.get("capital", 5_000.0)

    return {
        "risk_profile":      risk_profile,
        "risk_score":        total_score,
        "risk_max":          max_score,
        "horizon":           horizon_years,
        "capital":           capital,
        "capital_display":   answers.get("capital_display", f"USD {capital:,.0f}"),
        "income_stability":  answers.get("income_stability", ""),
        "loss_tolerance":    answers.get("loss_tolerance", ""),
        "objective":         answers.get("objective", ""),
        "experience":        answers.get("experience", ""),
        "emergency_fund":    answers.get("emergency_fund", ""),
        "raw_answers":       answers,
    }
