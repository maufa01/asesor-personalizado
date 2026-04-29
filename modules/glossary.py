"""
Glosario Financiero — definiciones educativas para inversores argentinos.
Lenguaje formal, ejemplos en pesos argentinos, nivel de riesgo por concepto.
"""

import streamlit as st

# ─── Datos ────────────────────────────────────────────────────────────────────

GLOSSARY = [
    {
        "category": "Instrumentos Financieros",
        "icon": "📈",
        "color": "#4fa3ff",
        "terms": [
            {
                "name": "Acciones",
                "risk_label": "Alto",
                "risk_color": "#ef4444",
                "definition": (
                    "Una acción representa una fracción de la propiedad de una empresa. "
                    "Al adquirirla, usted se convierte en socio de esa compañía y tiene derecho "
                    "a una parte de sus ganancias (dividendos) y a la valorización de su precio en el mercado. "
                    "Generan valor de dos formas: aumento del precio en bolsa y pago de dividendos."
                ),
                "example": (
                    "Si adquiere una acción de YPF (YPFD) a $25.000 y la empresa mejora sus resultados, "
                    "el precio puede subir a $32.000 en un año — una ganancia de $7.000 por acción (~28%). "
                    "También puede cobrar dividendos si la empresa los distribuye. "
                    "Ojo: si los resultados decepcionan, el precio puede caer por debajo de los $25.000."
                ),
            },
            {
                "name": "Bonos",
                "risk_label": "Bajo a Medio",
                "risk_color": "#f59e0b",
                "definition": (
                    "Un bono es un préstamo que usted le hace a un emisor (gobierno o empresa) a cambio "
                    "de pagos periódicos de interés (cupones) y la devolución del capital al vencimiento. "
                    "Existen dos tipos principales: "
                    "Bonos soberanos (emitidos por el Estado, ej. AL30, GD35) y "
                    "Bonos corporativos (emitidos por empresas privadas). "
                    "Los soberanos tienen mayor riesgo político en Argentina; los corporativos dependen "
                    "de la salud financiera de cada empresa."
                ),
                "example": (
                    "Si compra el AL30 (bono soberano en USD) a $350 pesos por unidad, "
                    "recibirá cupones semestrales en dólares y la devolución del capital. "
                    "A diferencia de una acción, el flujo de pagos es conocido de antemano, "
                    "lo que lo hace más predecible aunque no exento de riesgo de default."
                ),
            },
            {
                "name": "CEDEARs",
                "risk_label": "Medio a Alto",
                "risk_color": "#f59e0b",
                "definition": (
                    "Los Certificados de Depósito Argentinos (CEDEARs) son instrumentos que cotizan "
                    "en pesos en la bolsa argentina pero representan acciones o ETFs extranjeros "
                    "custodiados en el exterior. Permiten invertir en Apple, Amazon, Tesla, SPY o QQQ "
                    "sin necesidad de tener una cuenta en el exterior. "
                    "Su precio combina el valor del activo subyacente y el tipo de cambio implícito "
                    "(Dólar CCL), actuando como cobertura natural contra la devaluación del peso."
                ),
                "example": (
                    "Si el SPY (ETF del S&P 500) vale USD 500 y el dólar CCL está a $1.200, "
                    "el CEDEAR del SPY cotizará aproximadamente $600.000 por unidad (ajustado por ratio). "
                    "Si el peso se devalúa un 20%, el CEDEAR subirá en pesos aunque el SPY no se mueva, "
                    "protegiendo así el poder adquisitivo de su inversión."
                ),
            },
            {
                "name": "Letras del Tesoro (LECAPs)",
                "risk_label": "Bajo",
                "risk_color": "#22c55e",
                "definition": (
                    "Las LECAPs (Letras de Capitalización) son títulos de deuda a corto plazo "
                    "emitidos por el Tesoro Nacional argentino. Se emiten a descuento — es decir, "
                    "se compran por debajo de su valor nominal y al vencimiento se cobran a $100 — "
                    "y no pagan cupones periódicos. Son instrumentos en pesos y de corto plazo "
                    "(generalmente 30 a 270 días), ideales para estacionar liquidez en pesos "
                    "con tasa predecible."
                ),
                "example": (
                    "Si una LECAP con vencimiento a 90 días tiene una TNA del 60%, "
                    "usted paga aproximadamente $95 hoy y cobra $100 en 3 meses "
                    "(equivalente a un rendimiento del ~5,2% en ese período). "
                    "El riesgo principal es el riesgo soberano: si el Estado no paga, pierde el capital."
                ),
            },
            {
                "name": "Obligaciones Negociables (ONs)",
                "risk_label": "Medio",
                "risk_color": "#f59e0b",
                "definition": (
                    "Las Obligaciones Negociables son bonos corporativos emitidos por empresas privadas "
                    "argentinas para financiar sus operaciones. A diferencia de los bonos del Estado, "
                    "el emisor es una empresa (Pampa Energía, MercadoLibre, Arcor, Telecom, etc.). "
                    "Pagan cupones periódicos en dólares o pesos y devuelven el capital al vencimiento. "
                    "Son consideradas más seguras que los bonos soberanos argentinos "
                    "porque las empresas emisoras tienen activos concretos como respaldo."
                ),
                "example": (
                    "La ON de Pampa Energía (PCAHO) puede pagar una tasa del 9% anual en USD "
                    "con vencimiento en 5 años. Si invierte USD 1.000, recibirá USD 90 por año "
                    "en cupones y al vencimiento recuperará sus USD 1.000 — "
                    "siempre que Pampa Energía no incumpla sus obligaciones."
                ),
            },
            {
                "name": "Fondos Comunes de Inversión (FCI)",
                "risk_label": "Variable según tipo",
                "risk_color": "#60a5fa",
                "definition": (
                    "Un FCI agrupa el dinero de muchos inversores para invertirlo en conjunto, "
                    "administrado por una sociedad gerente profesional. Existen múltiples tipos: "
                    "Money Market (invierten en activos de muy corto plazo, rescate en el día, riesgo mínimo), "
                    "Renta Fija (invierten en bonos, mayor rendimiento, rescate en 24-48h), "
                    "Renta Variable (invierten en acciones, mayor riesgo y retorno). "
                    "La cuotaparte es la unidad de medida: su valor fluctúa con el mercado."
                ),
                "example": (
                    "En un FCI Money Market como el de Consultatio o Balanz, "
                    "si invierte $500.000 y la cuotaparte rinde un 80% anual TNA, "
                    "en 30 días habrá ganado aproximadamente $32.876 ($500.000 × 80%/365 × 30). "
                    "El rescate es el mismo día hábil, lo que lo convierte en una alternativa "
                    "al plazo fijo con mayor liquidez."
                ),
            },
            {
                "name": "ETFs (Exchange-Traded Funds)",
                "risk_label": "Medio a Alto",
                "risk_color": "#f59e0b",
                "definition": (
                    "Un ETF es un fondo que cotiza en bolsa como si fuera una acción, "
                    "replicando el comportamiento de un índice (S&P 500, Nasdaq, oro, etc.). "
                    "A diferencia de un FCI, el ETF se compra y vende en tiempo real durante la jornada, "
                    "tiene comisiones de gestión mucho más bajas y es totalmente transparente "
                    "en cuanto a sus activos subyacentes. "
                    "En Argentina se accede a ellos a través de CEDEARs."
                ),
                "example": (
                    "El SPY es el ETF del S&P 500 (las 500 empresas más grandes de EE.UU.). "
                    "Comprando un CEDEAR del SPY, usted replica automáticamente el rendimiento "
                    "de Apple, Microsoft, Amazon, Google y otras 496 empresas con una sola operación, "
                    "pagando una comisión de gestión de apenas el 0,0945% anual."
                ),
            },
        ],
    },
    {
        "category": "Conceptos Cambiarios",
        "icon": "💱",
        "color": "#10d98a",
        "terms": [
            {
                "name": "Dólar MEP (Mercado Electrónico de Pagos)",
                "risk_label": "Bajo — operación legal",
                "risk_color": "#22c55e",
                "definition": (
                    "El Dólar MEP es una forma legal de adquirir dólares en Argentina "
                    "a través del mercado de capitales, sin pasar por el cepo cambiario. "
                    "La operatoria consiste en: comprar un bono en pesos (ej. AL30), "
                    "esperar el período de parking obligatorio (1 día hábil), "
                    "y venderlo en su versión en dólares (AL30D). "
                    "La diferencia entre el precio de compra en pesos y venta en dólares "
                    "determina el tipo de cambio MEP."
                ),
                "example": (
                    "Si compra AL30 a $340 pesos y lo vende en dólares a USD 0,30, "
                    "el tipo de cambio implícito es $340 / 0,30 = $1.133/USD. "
                    "Esta operación es 100% legal, no requiere justificación de origen de fondos "
                    "y no tiene límite mensual — a diferencia del dólar oficial o el blue."
                ),
            },
            {
                "name": "Dólar CCL (Contado con Liquidación)",
                "risk_label": "Bajo — operación legal",
                "risk_color": "#22c55e",
                "definition": (
                    "El Dólar CCL (o 'Cable') es similar al MEP pero la venta del bono "
                    "se realiza en una cuenta en el exterior, por lo que los dólares "
                    "quedan depositados fuera de Argentina. "
                    "Es útil para transferir dólares al exterior legalmente. "
                    "Suele cotizar levemente más alto que el MEP porque implica "
                    "la salida física de divisas del sistema financiero argentino."
                ),
                "example": (
                    "Si el MEP está a $1.130/USD y el CCL a $1.160/USD, "
                    "la diferencia de $30 refleja el costo de sacar los dólares del país. "
                    "Conviene usar CCL cuando necesita dólares en el exterior "
                    "(cuenta bancaria internacional, inversiones en el exterior), "
                    "y MEP cuando prefiere tener los dólares en Argentina."
                ),
            },
            {
                "name": "Brecha Cambiaria",
                "risk_label": "Indicador — no es un instrumento",
                "risk_color": "#60a5fa",
                "definition": (
                    "La brecha cambiaria es la diferencia porcentual entre el tipo de cambio oficial "
                    "(el que fija el BCRA) y los tipos de cambio paralelos (MEP, CCL, blue). "
                    "Una brecha alta indica desconfianza en la política cambiaria y suele "
                    "generar incentivos para la dolarización de ahorros. "
                    "Afecta directamente a los CEDEARs: cuando la brecha sube, "
                    "los CEDEARs suben en pesos aunque el activo subyacente no se mueva."
                ),
                "example": (
                    "Si el dólar oficial está a $1.000 y el CCL a $1.200, "
                    "la brecha es del 20% ($200 / $1.000). "
                    "En ese contexto, un CEDEAR del SPY que no se movió en dólares "
                    "habrá subido un 20% medido en pesos solo por la ampliación de la brecha. "
                    "Cuando la brecha se comprime (cierra), ocurre el efecto contrario."
                ),
            },
        ],
    },
    {
        "category": "Conceptos de Mercado",
        "icon": "🏛️",
        "color": "#f0b429",
        "terms": [
            {
                "name": "BYMA (Bolsas y Mercados Argentinos)",
                "risk_label": "Informativo",
                "risk_color": "#64748b",
                "definition": (
                    "BYMA es la principal bolsa de valores de Argentina, donde se negocian "
                    "acciones, bonos, CEDEARs, ETFs, opciones y otros instrumentos financieros. "
                    "Opera en días hábiles de 11:00 a 17:00 hs (horario de verano). "
                    "Es una entidad autorizada y supervisada por la CNV (Comisión Nacional de Valores). "
                    "Todos los ALYCs operan a través de BYMA."
                ),
                "example": (
                    "Cuando usted compra CEDEARs de Apple a través de IOL o Balanz, "
                    "esa orden se ejecuta en el mercado BYMA, "
                    "donde miles de inversores compran y venden simultáneamente. "
                    "El precio que ve en la app es el último precio al que se cerró una operación en BYMA."
                ),
            },
            {
                "name": "ALYC (Agente de Liquidación y Compensación)",
                "risk_label": "Informativo",
                "risk_color": "#64748b",
                "definition": (
                    "Un ALYC es una sociedad de bolsa habilitada por la CNV para operar "
                    "en nombre de sus clientes en los mercados de capitales. "
                    "Son los intermediarios entre el inversor y BYMA. "
                    "Ejemplos en Argentina: IOL (InvertirOnline), Balanz, PPI (Portfolio Personal), "
                    "Bull Market, Cocos Capital. "
                    "Abrir una cuenta en un ALYC es gratuito y el proceso es 100% digital."
                ),
                "example": (
                    "Para abrir una cuenta en IOL: descargue la app, complete su información personal, "
                    "suba foto del DNI y selfie, firme el contrato digitalmente y espere la validación "
                    "(generalmente 24-48 horas hábiles). "
                    "Una vez aprobada, puede transferir pesos desde su banco y comenzar a operar."
                ),
            },
            {
                "name": "Plazo de Liquidación (T+0, T+1, T+2)",
                "risk_label": "Informativo",
                "risk_color": "#64748b",
                "definition": (
                    "El plazo de liquidación indica cuándo se acreditan efectivamente "
                    "los fondos o activos tras una operación. "
                    "T+0 (Contado Inmediato): liquidación el mismo día hábil. "
                    "T+1: liquidación al día hábil siguiente. "
                    "T+2: liquidación a los 2 días hábiles siguientes. "
                    "Los plazos afectan la liquidez disponible y son clave para el 'parking' del MEP."
                ),
                "example": (
                    "Si compra CEDEARs en T+2 el lunes, los títulos llegarán a su cuenta el miércoles. "
                    "Para el Dólar MEP, debe comprar el bono en T+1 y venderse en dólares en T+0 "
                    "(un día después), cumpliendo el parking obligatorio. "
                    "Los FCI Money Market rescatan en T+0, por lo que los fondos llegan el mismo día."
                ),
            },
            {
                "name": "Riesgo País (EMBI+)",
                "risk_label": "Indicador macroeconómico",
                "risk_color": "#60a5fa",
                "definition": (
                    "El riesgo país mide la diferencia (spread) entre el rendimiento de los bonos "
                    "de un país emergente y el de los bonos del Tesoro de EE.UU. (considerados libres de riesgo). "
                    "Se expresa en puntos básicos (pb): 100 pb = 1%. "
                    "Un riesgo país alto indica que el mercado percibe mayor probabilidad "
                    "de que el país no pague su deuda, por lo que exige mayor rendimiento "
                    "para prestarle dinero."
                ),
                "example": (
                    "Si el riesgo país de Argentina es 700 pb (7%), significa que los bonos argentinos "
                    "deben rendir un 7% más que los bonos del Tesoro de EE.UU. para ser atractivos. "
                    "Cuando el riesgo país baja (ej. de 1.500 a 700 pb), los bonos suben de precio "
                    "porque el mercado confía más en el país — como ocurrió en 2024."
                ),
            },
            {
                "name": "Inflación vs. Rendimiento Real",
                "risk_label": "Concepto esencial",
                "risk_color": "#60a5fa",
                "definition": (
                    "El rendimiento nominal es el porcentaje que muestra su inversión. "
                    "El rendimiento real es lo que efectivamente gana descontada la inflación. "
                    "Fórmula: Rendimiento Real = ((1 + Rend. Nominal) / (1 + Inflación)) − 1. "
                    "Si su inversión rinde el 80% anual pero la inflación es del 100%, "
                    "su rendimiento real es negativo: está perdiendo poder adquisitivo."
                ),
                "example": (
                    "Un plazo fijo al 60% TNA en un año de 100% de inflación: "
                    "$100.000 se convierten en $160.000 nominales, pero con inflación del 100% "
                    "ese dinero solo vale $80.000 en términos reales. "
                    "Rendimiento real ≈ (1,60 / 2,00) − 1 = −20%. "
                    "Por eso es fundamental buscar instrumentos que superen la inflación."
                ),
            },
        ],
    },
    {
        "category": "Conceptos de Cartera",
        "icon": "🧩",
        "color": "#a78bfa",
        "terms": [
            {
                "name": "Diversificación",
                "risk_label": "Estrategia de reducción del riesgo",
                "risk_color": "#22c55e",
                "definition": (
                    "Diversificar significa distribuir el capital entre distintos activos, "
                    "sectores, monedas y geografías para reducir el riesgo total de la cartera. "
                    "El principio: si un activo cae, los demás pueden compensarlo. "
                    "No se trata de tener muchos activos, sino de combinar activos "
                    "cuya correlación sea baja (que no caigan todos al mismo tiempo)."
                ),
                "example": (
                    "Una cartera 100% en acciones argentinas concentra todo el riesgo en el país. "
                    "Si distribuye entre CEDEARs internacionales (40%), bonos en USD (30%), "
                    "dólar MEP (20%) y acciones locales (10%), una crisis argentina "
                    "afecta solo al 10% de su cartera, mientras el resto puede mantenerse estable o subir."
                ),
            },
            {
                "name": "Rebalanceo",
                "risk_label": "Práctica periódica recomendada",
                "risk_color": "#60a5fa",
                "definition": (
                    "El rebalanceo es el proceso de ajustar periódicamente la cartera "
                    "para volver a los pesos originales de cada activo. "
                    "Con el tiempo, los activos que más subieron representan una porción mayor "
                    "de lo planificado, aumentando el riesgo involuntariamente. "
                    "Rebalancear implica vender lo que subió más y comprar lo que quedó rezagado "
                    "(o agregar nuevo capital al activo sub-representado)."
                ),
                "example": (
                    "Usted arma una cartera 50% bonos / 50% CEDEARs. "
                    "Al cabo de un año, los CEDEARs subieron 40% y los bonos solo 10%. "
                    "Ahora su cartera es 44% bonos / 56% CEDEARs. "
                    "Al rebalancear, vende parte de los CEDEARs y compra bonos para volver al 50/50. "
                    "Se recomienda rebalancear cada 6 a 12 meses."
                ),
            },
            {
                "name": "Horizonte Temporal",
                "risk_label": "Factor clave en la estrategia",
                "risk_color": "#60a5fa",
                "definition": (
                    "El horizonte temporal es el período durante el cual usted puede mantener "
                    "su inversión sin necesitar ese dinero. "
                    "Es uno de los factores más importantes para definir qué activos son adecuados. "
                    "A mayor horizonte, mayor capacidad de asumir riesgo y esperar recuperaciones. "
                    "A menor horizonte, priorizar liquidez y preservación del capital."
                ),
                "example": (
                    "Si necesita el dinero en 6 meses, no debería invertir en acciones: "
                    "una caída del 30% en ese período podría obligarlo a vender con pérdida. "
                    "En cambio, si su horizonte es de 10 años, una caída del 30% es una oportunidad "
                    "para comprar más barato, ya que históricamente los mercados se recuperan "
                    "y superan máximos en plazos de 3 a 7 años."
                ),
            },
            {
                "name": "Perfil de Riesgo",
                "risk_label": "Clasificación personal",
                "risk_color": "#60a5fa",
                "definition": (
                    "El perfil de riesgo es la clasificación que refleja su tolerancia "
                    "a la volatilidad y potencial pérdida de su capital. "
                    "Se determina combinando factores como: horizonte temporal, "
                    "estabilidad de ingresos, fondo de emergencia, experiencia previa "
                    "y reacción emocional ante pérdidas. "
                    "Conservador: prioriza seguridad. "
                    "Estable: algo mejor que el plazo fijo con riesgo controlado. "
                    "Moderado: equilibrio entre crecimiento y protección. "
                    "Agresivo: maximiza el rendimiento asumiendo alta volatilidad."
                ),
                "example": (
                    "Un inversor conservador con $1.000.000 podría tener: "
                    "60% en FCI Money Market ($600.000), 25% en bonos CER ($250.000) "
                    "y 15% en dólar MEP ($150.000). "
                    "Un inversor agresivo podría tener: 50% en CEDEARs de tecnología, "
                    "25% en acciones argentinas y 25% en bonos en USD. "
                    "Ninguno es mejor: depende de sus objetivos y su situación particular."
                ),
            },
        ],
    },
]


# ─── Render ───────────────────────────────────────────────────────────────────

def render_glossary():
    """Renderiza la página completa del Glosario Financiero."""

    # ── Botón Volver ─────────────────────────────────────────────────────────
    col_back, _ = st.columns([1, 5])
    with col_back:
        if st.button("← Volver", key="glosario_back", use_container_width=True):
            prev = st.session_state.get("_prev_step", "intro")
            st.session_state.step = prev
            st.rerun()

    # ── Encabezado ───────────────────────────────────────────────────────────
    st.markdown("""
<div class="glosario-header">
  <div class="glosario-icon">📚</div>
  <h1 class="glosario-title">Glosario Financiero</h1>
  <p class="glosario-sub">
    Definiciones claras de los conceptos del mercado de capitales argentino.<br>
    Cada término incluye una definición, un ejemplo práctico y su nivel de riesgo.
  </p>
</div>
""", unsafe_allow_html=True)

    # ── Barra de búsqueda ────────────────────────────────────────────────────
    search = st.text_input(
        label="Buscar concepto",
        placeholder="🔍  Escriba un término para buscar... (ej: CEDEAR, MEP, diversificación)",
        key="glossary_search",
        label_visibility="collapsed",
    )
    query = search.strip().lower()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Categorías y términos ─────────────────────────────────────────────────
    total_matches = 0

    for cat in GLOSSARY:
        # Filtrar términos según búsqueda
        if query:
            matching = [
                t for t in cat["terms"]
                if query in t["name"].lower() or query in t["definition"].lower() or query in t["example"].lower()
            ]
        else:
            matching = cat["terms"]

        if not matching:
            continue

        total_matches += len(matching)

        # Cabecera de categoría
        st.markdown(f"""
<div class="glosario-cat-header" style="border-left-color:{cat['color']};">
  <span class="glosario-cat-icon">{cat['icon']}</span>
  <span class="glosario-cat-title">{cat['category']}</span>
  <span class="glosario-cat-count">{len(matching)} término{"s" if len(matching) != 1 else ""}</span>
</div>
""", unsafe_allow_html=True)

        for term in matching:
            _render_term(term, cat["color"])

        st.markdown("<br>", unsafe_allow_html=True)

    # Mensaje cuando no hay resultados
    if query and total_matches == 0:
        st.markdown(f"""
<div class="glosario-empty">
  <div style="font-size:2rem;margin-bottom:0.8rem">🔍</div>
  <p>No se encontraron resultados para <strong>"{search}"</strong>.</p>
  <p style="color:var(--text-3);font-size:0.9rem;">Intente con términos como: acción, bono, CEDEAR, MEP, diversificación, riesgo...</p>
</div>
""", unsafe_allow_html=True)


def _render_term(term: dict, cat_color: str):
    """Renderiza un término individual como expander."""
    risk_label = term["risk_label"]
    risk_color = term["risk_color"]

    label = f"{term['name']}"

    with st.expander(label, expanded=False):
        # Badge de riesgo
        st.markdown(f"""
<div style="margin-bottom:1rem;">
  <span class="risk-badge" style="background:{risk_color}22;color:{risk_color};border:1px solid {risk_color}66;">
    ⚡ Nivel de riesgo: {risk_label}
  </span>
</div>
""", unsafe_allow_html=True)

        # Definición
        st.markdown(f"""
<div class="glosario-definition">
  <div class="glosario-def-label">Definición</div>
  <p class="glosario-def-text">{term['definition']}</p>
</div>
""", unsafe_allow_html=True)

        # Ejemplo
        st.markdown(f"""
<div class="glosario-example">
  <div class="glosario-example-label">📌 Ejemplo práctico en Argentina</div>
  <p class="glosario-example-text">{term['example']}</p>
</div>
""", unsafe_allow_html=True)
