"""
Motor de construcción de carteras
Genera asignaciones diversificadas según perfil de riesgo,
con activos del mercado argentino e internacional.
"""

from typing import List, Dict, Any


# ─── Universo de activos ───────────────────────────────────────────────────────
ASSET_UNIVERSE: List[Dict[str, Any]] = [

    # ══ PESOS ARGENTINOS — baja volatilidad ════════════════════════════════════

    {
        "id": "cash_pesos",
        "name": "Cuenta Remunerada (Naranja X / Ualá)",
        "category": "Pesos ARS",
        "sub": "Liquidez",
        "ticker": "ARS",
        "color": "#94a3b8",
        "expected_return": 0.03,
        "volatility": 0.01,
        "risk_level": "mínimo",
        "description": "Plata disponible al instante en cuentas como Naranja X o Ualá que pagan interés diario automático. No hacés nada: el dinero rinde solo mientras está ahí. Retiro en cualquier momento, sin costo.",
        "currency": "ARS",
        "market": "Banco",
        "simple_desc": "Dinero en Naranja X o Ualá rindiendo interés diario, retiro inmediato",
    },
    {
        "id": "money_market",
        "name": "Fondo Money Market (Consultatio / Balanz)",
        "category": "Pesos ARS",
        "sub": "Fondos CLP",
        "ticker": "FCI-MM",
        "color": "#a3e635",
        "expected_return": 0.05,
        "volatility": 0.01,
        "risk_level": "mínimo",
        "description": "Fondos como Consultatio Money Market (disponible en IOL) o Balanz Money Market. Invierten en plazos fijos bancarios y letras de cortísimo plazo. Retiro el mismo día, rinden más que un plazo fijo tradicional. También accesible desde Mercado Pago o Ualá como 'cuenta de inversión'.",
        "currency": "ARS",
        "market": "FCI",
        "simple_desc": "Consultatio o Balanz Money Market: retiro el mismo día, más que un plazo fijo",
    },
    {
        "id": "plazo_fijo",
        "name": "Plazo Fijo 30 días (Banco Galicia / Santander)",
        "category": "Pesos ARS",
        "sub": "Ahorro bancario",
        "ticker": "PF",
        "color": "#84cc16",
        "expected_return": 0.06,
        "volatility": 0.02,
        "risk_level": "mínimo",
        "description": "Plazo fijo a 30 días en bancos como Galicia, Santander o BBVA. Tasa fija garantizada, sin riesgo de precio. Cubierto por el Fondo de Garantía de Depósitos hasta $20 millones. La pega: no podés sacarlo antes del vencimiento.",
        "currency": "ARS",
        "market": "Banco",
        "simple_desc": "Plazo fijo 30 días en Galicia o Santander, garantizado por el banco",
    },
    {
        "id": "fci_t0",
        "name": "Fondo Renta Fija T+0 (Balanz / PPI)",
        "category": "Pesos ARS",
        "sub": "Fondos CLP",
        "ticker": "FCI-T0",
        "color": "#65a30d",
        "expected_return": 0.07,
        "volatility": 0.02,
        "risk_level": "muy bajo",
        "description": "Fondos como Balanz Renta Fija o el fondo T+0 de PPI. Invierten en letras y bonos de corto plazo en pesos. Retiro el mismo día hábil. Un escalón más de rendimiento que el money market puro, con riesgo casi igual.",
        "currency": "ARS",
        "market": "FCI",
        "simple_desc": "Balanz o PPI Renta Fija: retiro el mismo día, mejor rendimiento que money market",
    },
    {
        "id": "lecap",
        "name": "LECAPs del Tesoro (S31M26 / S30J26)",
        "category": "Pesos ARS",
        "sub": "Deuda Pública ARS",
        "ticker": "LECAP",
        "color": "#4ade80",
        "expected_return": 0.08,
        "volatility": 0.04,
        "risk_level": "bajo",
        "description": "Letras del Tesoro argentino a tasa fija. Las más operadas son la S31M26 (vence 31 marzo 2026) y S30J26 (vence 30 junio 2026). Se compran en IOL, PPI o Balanz como si fuera una acción. Riesgo: si el gobierno no paga, se pierde. Por eso solo una parte de la cartera va acá.",
        "currency": "ARS",
        "market": "BYMA",
        "simple_desc": "S31M26 o S30J26: letras del Tesoro a tasa fija, comprables en IOL o PPI",
    },
    {
        "id": "cer_bond",
        "name": "Bono CER TX26 / TX28 (ajusta por inflación)",
        "category": "Pesos ARS",
        "sub": "Deuda Pública ARS",
        "ticker": "CER",
        "color": "#22c55e",
        "expected_return": 0.09,
        "volatility": 0.06,
        "risk_level": "bajo",
        "description": "TX26 (vence julio 2026) o TX28 (vence julio 2028): bonos del Tesoro que ajustan por el índice de inflación (CER) más una tasa extra. Si la inflación es 100%, estos bonos valen 100% más. Son la mejor cobertura en pesos contra la inflación. Comprables en IOL, PPI o Balanz.",
        "currency": "ARS",
        "market": "BYMA",
        "simple_desc": "TX26 o TX28: bono que sube con la inflación, comprá en IOL o PPI",
    },
    {
        "id": "fci_renta_pesos",
        "name": "Fondo Renta Fija Pesos (Consultatio / SBS)",
        "category": "Pesos ARS",
        "sub": "Fondos CLP",
        "ticker": "FCI-RF",
        "color": "#16a34a",
        "expected_return": 0.09,
        "volatility": 0.05,
        "risk_level": "bajo",
        "description": "Fondos como Consultatio Renta Fija o SBS Renta Pesos. Invierten en una mezcla de LECAPs, bonos CER y otros instrumentos en pesos. Un gestor profesional decide la combinación exacta. Ideal para quien no quiere elegir bonos individuales.",
        "currency": "ARS",
        "market": "FCI",
        "simple_desc": "Consultatio o SBS Renta Fija: mezcla de bonos en pesos, manejada por expertos",
    },

    # ══ DÓLAR MEP Y COBERTURA ══════════════════════════════════════════════════

    {
        "id": "mep",
        "name": "Dólar MEP (vía AL30 en IOL o PPI)",
        "category": "Dólar MEP",
        "sub": "Reserva de valor",
        "ticker": "USD-MEP",
        "color": "#38bdf8",
        "expected_return": 0.00,
        "volatility": 0.08,
        "risk_level": "muy bajo",
        "description": "Dólares legales comprados a través de la bolsa sin límite mensual. El proceso: comprás el bono AL30 en pesos y lo vendés en dólares — queda una diferencia que es el 'tipo de cambio MEP'. IOL y PPI lo hacen automático en 1 click. El dólar queda en tu cuenta del broker en USD.",
        "currency": "USD",
        "market": "BYMA",
        "simple_desc": "Dólares legales por la bolsa, 1 click en IOL o PPI, sin límite mensual",
    },

    # ══ BONOS SOBERANOS USD ════════════════════════════════════════════════════

    {
        "id": "al30",
        "name": "Bono AL30 — soberano USD ley argentina",
        "category": "Bonos USD",
        "sub": "Soberano ARG",
        "ticker": "AL30",
        "color": "#0ea5e9",
        "expected_return": 0.10,
        "volatility": 0.18,
        "risk_level": "medio",
        "description": "El bono soberano argentino en dólares más líquido. Vence en 2030 y paga cupones semestrales en USD. Ley argentina. Compralo en IOL, PPI o Balanz. Riesgo real: si Argentina entra en default como en 2001, puede no pagarse. Por eso es solo una parte de la cartera.",
        "currency": "USD",
        "market": "BYMA",
        "simple_desc": "AL30: bono del gobierno argentino en USD, cupones semestrales, comprá en IOL",
    },
    {
        "id": "gd30",
        "name": "Bono GD30 — soberano USD ley Nueva York",
        "category": "Bonos USD",
        "sub": "Soberano ARG",
        "ticker": "GD30",
        "color": "#0284c7",
        "expected_return": 0.10,
        "volatility": 0.17,
        "risk_level": "medio",
        "description": "Igual que el AL30 pero bajo ley de Nueva York. Eso significa que si Argentina no paga, podés ir a juicio en EE.UU. — más protección legal. Es el bono soberano que más compran los fondos internacionales. Algo más caro que el AL30 por esa razón.",
        "currency": "USD",
        "market": "BYMA",
        "simple_desc": "GD30: igual que AL30 pero con protección legal en NY, preferido por fondos",
    },

    # ══ OBLIGACIONES NEGOCIABLES ════════════════════════════════════════════════

    {
        "id": "on_ypf",
        "name": "ON YPF 2026 (YPFDS) — deuda YPF en USD",
        "category": "Bonos USD",
        "sub": "Corporativo",
        "ticker": "YPFDS",
        "color": "#0369a1",
        "expected_return": 0.09,
        "volatility": 0.10,
        "risk_level": "bajo-medio",
        "description": "La obligación negociable YPFDS: YPF te pide prestados dólares y te devuelve el capital más intereses. Menor riesgo que comprar la acción de YPF porque en caso de quiebra los bonistas cobran antes que los accionistas. Comprala en IOL o PPI buscando el ticker YPFDS.",
        "currency": "USD",
        "market": "BYMA",
        "simple_desc": "YPFDS: YPF te paga intereses en dólares, menos riesgo que la acción",
    },
    {
        "id": "on_corp",
        "name": "ONs Corporativas (Pampa / Arcor / MercadoLibre)",
        "category": "Bonos USD",
        "sub": "Corporativo",
        "ticker": "ON-MIX",
        "color": "#075985",
        "expected_return": 0.08,
        "volatility": 0.08,
        "risk_level": "bajo-medio",
        "description": "Mezcla de obligaciones negociables de empresas privadas argentinas: Pampa Energía (PTSTO), Arcor, Tecpetrol (TCCUD), MercadoLibre. Todas pagan en dólares. Son consideradas más seguras que los bonos soberanos porque empresas privadas tienen mejor historial de pago que el Estado.",
        "currency": "USD",
        "market": "BYMA",
        "simple_desc": "ONs de Pampa, Arcor o MercadoLibre: empresas privadas que pagan en USD",
    },

    # ══ OBLIGACIONES NEGOCIABLES ADICIONALES ══════════════════════════════════

    {
        "id": "on_pampa",
        "name": "ON Pampa Energía (PTSTO)",
        "category": "Bonos USD",
        "sub": "Corporativo",
        "ticker": "PTSTO",
        "color": "#0c4a6e",
        "expected_return": 0.09,
        "volatility": 0.09,
        "risk_level": "bajo-medio",
        "description": "Obligación negociable de Pampa Energía en dólares. Una de las ONs más líquidas del mercado argentino. Rinde en USD con respaldo de activos energéticos.",
        "currency": "USD",
        "market": "BYMA",
        "simple_desc": "Deuda de Pampa Energía en dólares, muy líquida",
    },
    {
        "id": "on_tecpetrol",
        "name": "ON Tecpetrol (TCCUD)",
        "category": "Bonos USD",
        "sub": "Corporativo",
        "ticker": "TCCUD",
        "color": "#0c4a6e",
        "expected_return": 0.09,
        "volatility": 0.09,
        "risk_level": "bajo-medio",
        "description": "Obligación negociable de Tecpetrol (grupo Techint) en dólares. Empresa de petróleo y gas con sólidos fundamentos. Buena opción para renta en USD.",
        "currency": "USD",
        "market": "BYMA",
        "simple_desc": "Deuda de Tecpetrol en dólares, respaldo del grupo Techint",
    },

    # ══ CEDEARs TECNOLOGÍA ═════════════════════════════════════════════════════

    {
        "id": "aapl",
        "name": "Apple (AAPL)",
        "category": "CEDEARs",
        "sub": "Tecnología",
        "ticker": "AAPL",
        "color": "#a78bfa",
        "expected_return": 0.12,
        "volatility": 0.24,
        "risk_level": "medio",
        "description": "La empresa más grande del mundo. Hace iPhones, Macs y servicios digitales. Estable, con buen crecimiento histórico.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "La empresa de Apple, una de las más valiosas del mundo",
    },
    {
        "id": "msft",
        "name": "Microsoft (MSFT)",
        "category": "CEDEARs",
        "sub": "Tecnología",
        "ticker": "MSFT",
        "color": "#8b5cf6",
        "expected_return": 0.13,
        "volatility": 0.23,
        "risk_level": "medio",
        "description": "Gigante tech: Windows, Office, Azure (nube) y GitHub. Muy diversificada y estable. Una de las empresas más rentables del mundo.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "La empresa de Windows, Office y la nube Azure",
    },
    {
        "id": "googl",
        "name": "Alphabet / Google (GOOGL)",
        "category": "CEDEARs",
        "sub": "Tecnología",
        "ticker": "GOOGL",
        "color": "#7c3aed",
        "expected_return": 0.13,
        "volatility": 0.25,
        "risk_level": "medio",
        "description": "Dueña de Google, YouTube y Android. Domina publicidad digital. Gigantesca generación de caja y crecimiento sostenido.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "La empresa detrás de Google, YouTube y Android",
    },
    {
        "id": "amzn",
        "name": "Amazon (AMZN)",
        "category": "CEDEARs",
        "sub": "Consumo/Tech",
        "ticker": "AMZN",
        "color": "#6d28d9",
        "expected_return": 0.14,
        "volatility": 0.27,
        "risk_level": "medio-alto",
        "description": "Comercio electrónico y nube (AWS). Dos negocios enormes en uno. Alto potencial de crecimiento.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "Amazon: tienda online + la nube más grande del mundo",
    },
    {
        "id": "nvda",
        "name": "Nvidia (NVDA)",
        "category": "CEDEARs",
        "sub": "Tecnología/IA",
        "ticker": "NVDA",
        "color": "#5b21b6",
        "expected_return": 0.22,
        "volatility": 0.48,
        "risk_level": "alto",
        "description": "Fabricante de chips para inteligencia artificial. El negocio creció exponencialmente con el boom de la IA. Alta volatilidad.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "La empresa de chips para inteligencia artificial",
    },
    {
        "id": "meli",
        "name": "MercadoLibre (MELI)",
        "category": "CEDEARs",
        "sub": "Tecnología LATAM",
        "ticker": "MELI",
        "color": "#4f46e5",
        "expected_return": 0.20,
        "volatility": 0.38,
        "risk_level": "alto",
        "description": "Líder en e-commerce y fintech en Latinoamérica. Opera en Argentina, Brasil, México. Alto potencial y alta volatilidad.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "MercadoLibre: la empresa de comercio y pagos online más grande de Latinoamérica",
    },

    {
        "id": "meta",
        "name": "Meta / Facebook (META)",
        "category": "CEDEARs",
        "sub": "Tecnología",
        "ticker": "META",
        "color": "#1d4ed8",
        "expected_return": 0.15,
        "volatility": 0.28,
        "risk_level": "medio-alto",
        "description": "Dueña de Facebook, Instagram y WhatsApp. Domina publicidad digital global. Apuesta fuerte a la inteligencia artificial.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "La empresa de Facebook, Instagram y WhatsApp",
    },
    {
        "id": "brk",
        "name": "Berkshire Hathaway (BRK/B)",
        "category": "CEDEARs",
        "sub": "Financiero",
        "ticker": "BRKB",
        "color": "#92400e",
        "expected_return": 0.11,
        "volatility": 0.18,
        "risk_level": "medio",
        "description": "Holding de Warren Buffett. Dueña de decenas de empresas: seguros, energía, consumo, bancos. La más diversificada del mundo en un solo activo.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "El holding de Warren Buffett, muy diversificado y sólido",
    },
    {
        "id": "jpm",
        "name": "JPMorgan Chase (JPM)",
        "category": "CEDEARs",
        "sub": "Financiero",
        "ticker": "JPM",
        "color": "#1e3a5f",
        "expected_return": 0.12,
        "volatility": 0.22,
        "risk_level": "medio",
        "description": "El banco más grande de EE.UU. por activos. Muy sólido, paga dividendos y se beneficia de tasas altas. Referente del sector financiero global.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "El banco más grande de EE.UU., sólido y con dividendos",
    },

    # ══ CEDEARs CONSUMO & SALUD ════════════════════════════════════════════════

    {
        "id": "ko",
        "name": "Coca-Cola (KO)",
        "category": "CEDEARs",
        "sub": "Consumo Masivo",
        "ticker": "KO",
        "color": "#dc2626",
        "expected_return": 0.08,
        "volatility": 0.14,
        "risk_level": "medio",
        "description": "Marca global de bebidas. Paga dividendos históricos, muy estable. Ideal para carteras defensivas que buscan ingreso pasivo.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Coca-Cola: estable, global y paga dividendos hace décadas",
    },
    {
        "id": "wmt",
        "name": "Walmart (WMT)",
        "category": "CEDEARs",
        "sub": "Consumo Masivo",
        "ticker": "WMT",
        "color": "#b91c1c",
        "expected_return": 0.09,
        "volatility": 0.15,
        "risk_level": "medio",
        "description": "Mayor cadena de supermercados del mundo. Muy resistente a recesiones. También tiene e-commerce creciente.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "El supermercado más grande del mundo, muy estable",
    },
    {
        "id": "jnj",
        "name": "Johnson & Johnson (JNJ)",
        "category": "CEDEARs",
        "sub": "Salud",
        "ticker": "JNJ",
        "color": "#991b1b",
        "expected_return": 0.08,
        "volatility": 0.13,
        "risk_level": "bajo-medio",
        "description": "Empresa farmacéutica y de productos de salud. Muy defensiva, paga dividendos crecientes hace más de 60 años.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Farmacéutica gigante, muy estable y con dividendos históricos",
    },
    {
        "id": "pfe",
        "name": "Pfizer (PFE)",
        "category": "CEDEARs",
        "sub": "Salud",
        "ticker": "PFE",
        "color": "#7f1d1d",
        "expected_return": 0.07,
        "volatility": 0.20,
        "risk_level": "medio",
        "description": "Laboratorio farmacéutico global. Conocido por la vacuna COVID. Pipeline amplio de medicamentos.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Pfizer, uno de los laboratorios más grandes del mundo",
    },

    # ══ CEDEARs ENERGÍA ════════════════════════════════════════════════════════

    {
        "id": "xom",
        "name": "ExxonMobil (XOM)",
        "category": "CEDEARs",
        "sub": "Energía",
        "ticker": "XOM",
        "color": "#ea580c",
        "expected_return": 0.09,
        "volatility": 0.22,
        "risk_level": "medio",
        "description": "Gigante petrolero y gasífero estadounidense. Se beneficia cuando sube el precio del crudo. Paga buenos dividendos.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "ExxonMobil: petróleo y gas, con buenos dividendos",
    },
    {
        "id": "tsla",
        "name": "Tesla (TSLA)",
        "category": "CEDEARs",
        "sub": "Tecnología/Autos",
        "ticker": "TSLA",
        "color": "#c2410c",
        "expected_return": 0.18,
        "volatility": 0.55,
        "risk_level": "alto",
        "description": "Líder en autos eléctricos. Alto potencial de crecimiento pero muy volátil. Puede subir o bajar 20% en semanas.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "Tesla: autos eléctricos, muy volátil pero con alto potencial",
    },

    # ══ CEDEARs FINANZAS & INDUSTRIA ══════════════════════════════════════════

    {
        "id": "bac",
        "name": "Bank of America (BAC)",
        "category": "CEDEARs",
        "sub": "Financiero",
        "ticker": "BAC",
        "color": "#dc2626",
        "expected_return": 0.11,
        "volatility": 0.25,
        "risk_level": "medio",
        "description": "Segundo banco de EE.UU. por activos. Exposición al ciclo económico americano, banca retail y corporativa.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Bank of America, uno de los bancos más grandes del mundo",
    },
    {
        "id": "dis",
        "name": "Walt Disney (DIS)",
        "category": "CEDEARs",
        "sub": "Consumo/Entretenimiento",
        "ticker": "DIS",
        "color": "#1d4ed8",
        "expected_return": 0.10,
        "volatility": 0.25,
        "risk_level": "medio",
        "description": "La empresa del entretenimiento más famosa del mundo. Dueña de Disney+, Marvel, Star Wars, ESPN y parques temáticos.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Disney: películas, streaming, parques y Marvel",
    },

    # ══ ETFs GLOBALES (via CEDEAR) ═════════════════════════════════════════════

    {
        "id": "spy",
        "name": "ETF S&P 500 (SPY)",
        "category": "ETFs",
        "sub": "Índice USA",
        "ticker": "SPY",
        "color": "#10d98a",
        "expected_return": 0.11,
        "volatility": 0.17,
        "risk_level": "medio",
        "description": "Replica las 500 empresas más grandes de EE.UU. Apple, Microsoft, Amazon, Google... todas juntas en una sola inversión. Muy recomendado para principiantes.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Las 500 empresas más grandes de EE.UU. en una sola compra",
    },
    {
        "id": "qqq",
        "name": "ETF Nasdaq 100 (QQQ)",
        "category": "ETFs",
        "sub": "Índice Tech USA",
        "ticker": "QQQ",
        "color": "#059669",
        "expected_return": 0.14,
        "volatility": 0.22,
        "risk_level": "medio-alto",
        "description": "Replica las 100 empresas tecnológicas del Nasdaq. Más crecimiento que el S&P 500 pero con mayor volatilidad.",
        "currency": "USD",
        "market": "BYMA/NASDAQ",
        "simple_desc": "Las 100 empresas tech más grandes de EE.UU.",
    },
    {
        "id": "eem",
        "name": "ETF Mercados Emergentes (EEM)",
        "category": "ETFs",
        "sub": "Emergentes Global",
        "ticker": "EEM",
        "color": "#047857",
        "expected_return": 0.09,
        "volatility": 0.20,
        "risk_level": "medio",
        "description": "Exposición a economías emergentes: China, India, Brasil, México, Corea. Diversificación geográfica amplia.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Acceso a economías emergentes de todo el mundo",
    },
    {
        "id": "iau",
        "name": "ETF Oro (IAU)",
        "category": "ETFs",
        "sub": "Commodities",
        "ticker": "IAU",
        "color": "#d97706",
        "expected_return": 0.06,
        "volatility": 0.14,
        "risk_level": "bajo-medio",
        "description": "Fondo que replica el precio del oro. Reserva de valor histórica, protege en momentos de crisis. No paga dividendos.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Invertir en oro sin necesidad de comprarlo físicamente",
    },

    {
        "id": "vti",
        "name": "ETF Mercado Total USA (VTI)",
        "category": "ETFs",
        "sub": "Índice USA",
        "ticker": "VTI",
        "color": "#0d9488",
        "expected_return": 0.11,
        "volatility": 0.17,
        "risk_level": "medio",
        "description": "Replica todo el mercado bursátil de EE.UU.: más de 3.800 empresas en un solo fondo. Más diversificado que el SPY.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Todo el mercado americano en una sola inversión",
    },
    {
        "id": "gld",
        "name": "ETF Oro (GLD)",
        "category": "ETFs",
        "sub": "Commodities",
        "ticker": "GLD",
        "color": "#ca8a04",
        "expected_return": 0.06,
        "volatility": 0.14,
        "risk_level": "bajo-medio",
        "description": "El ETF de oro más grande del mundo. Reserva de valor clásica, descorrelacionado de acciones. Sube en momentos de crisis e incertidumbre.",
        "currency": "USD",
        "market": "BYMA/NYSE",
        "simple_desc": "Oro físico respaldado, el refugio anti-crisis clásico",
    },

    # ══ ACCIONES ARGENTINAS ════════════════════════════════════════════════════

    {
        "id": "ypf",
        "name": "YPF (YPFD)",
        "category": "Acciones ARG",
        "sub": "Energía ARG",
        "ticker": "YPFD",
        "color": "#f59e0b",
        "expected_return": 0.18,
        "volatility": 0.45,
        "risk_level": "alto",
        "description": "Empresa estatal petrolera argentina. Muy volátil pero con alto potencial si Argentina crece. Ligada al proyecto Vaca Muerta.",
        "currency": "ARS",
        "market": "BYMA",
        "simple_desc": "La petrolera estatal argentina, ligada a Vaca Muerta",
    },
    {
        "id": "galicia",
        "name": "Banco Galicia (GGAL)",
        "category": "Acciones ARG",
        "sub": "Financiero ARG",
        "ticker": "GGAL",
        "color": "#ef4444",
        "expected_return": 0.20,
        "volatility": 0.50,
        "risk_level": "alto",
        "description": "Uno de los bancos privados más grandes de Argentina. Muy sensible al ciclo económico local. Alto riesgo y alto potencial.",
        "currency": "ARS",
        "market": "BYMA",
        "simple_desc": "Banco Galicia, uno de los mayores bancos privados argentinos",
    },
    {
        "id": "teco2",
        "name": "Telecom Argentina (TECO2)",
        "category": "Acciones ARG",
        "sub": "Telecomunicaciones ARG",
        "ticker": "TECO2",
        "color": "#3b82f6",
        "expected_return": 0.15,
        "volatility": 0.38,
        "risk_level": "alto",
        "description": "Empresa de telecomunicaciones líder en Argentina. Ofrece internet, telefonía y TV. Más defensiva que YPF o bancos.",
        "currency": "ARS",
        "market": "BYMA",
        "simple_desc": "Telecom Argentina, líder en internet y telefonía",
    },
    {
        "id": "pampa",
        "name": "Pampa Energía (PAMP)",
        "category": "Acciones ARG",
        "sub": "Energía ARG",
        "ticker": "PAMP",
        "color": "#f97316",
        "expected_return": 0.17,
        "volatility": 0.42,
        "risk_level": "alto",
        "description": "Empresa energética argentina. Genera electricidad y tiene negocios en gas. Ligada al desarrollo energético del país.",
        "currency": "ARS",
        "market": "BYMA",
        "simple_desc": "Pampa Energía, empresa de electricidad y gas argentina",
    },

    {
        "id": "vist",
        "name": "Vista Energy (VIST)",
        "category": "Acciones ARG",
        "sub": "Energía ARG",
        "ticker": "VIST",
        "color": "#b45309",
        "expected_return": 0.22,
        "volatility": 0.48,
        "risk_level": "alto",
        "description": "Empresa de petróleo y gas con foco en Vaca Muerta. Una de las de mayor crecimiento en Argentina. Cotiza en NYSE y BYMA.",
        "currency": "ARS",
        "market": "BYMA/NYSE",
        "simple_desc": "Vista Energy: petróleo de Vaca Muerta, alta proyección",
    },
    {
        "id": "bbar",
        "name": "Banco BBVA Argentina (BBAR)",
        "category": "Acciones ARG",
        "sub": "Financiero ARG",
        "ticker": "BBAR",
        "color": "#0891b2",
        "expected_return": 0.18,
        "volatility": 0.48,
        "risk_level": "alto",
        "description": "Filial argentina del BBVA, uno de los bancos privados más grandes del país. Muy sensible al ciclo económico argentino.",
        "currency": "ARS",
        "market": "BYMA",
        "simple_desc": "Banco BBVA Argentina, uno de los mayores bancos privados",
    },
    {
        "id": "loma",
        "name": "Loma Negra (LOMA)",
        "category": "Acciones ARG",
        "sub": "Industria ARG",
        "ticker": "LOMA",
        "color": "#78716c",
        "expected_return": 0.14,
        "volatility": 0.40,
        "risk_level": "alto",
        "description": "La cementera más grande de Argentina. Se beneficia del crecimiento en construcción e infraestructura. Más defensiva que bancos o petroleras.",
        "currency": "ARS",
        "market": "BYMA",
        "simple_desc": "Loma Negra: la cementera más grande de Argentina",
    },

    # ══ CRIPTOMONEDAS ══════════════════════════════════════════════════════════

    {
        "id": "btc",
        "name": "Bitcoin (BTC)",
        "category": "Cripto",
        "sub": "Cripto principal",
        "ticker": "BTC",
        "color": "#f97316",
        "expected_return": 0.25,
        "volatility": 0.70,
        "risk_level": "alto",
        "description": "La criptomoneda más conocida y de mayor capitalización. Muy volátil pero con crecimiento histórico enorme. Solo apta para perfil agresivo.",
        "currency": "USD",
        "market": "Exchanges",
        "simple_desc": "Bitcoin: la crypto más conocida, alto riesgo y alto potencial",
    },
    {
        "id": "eth",
        "name": "Ethereum (ETH)",
        "category": "Cripto",
        "sub": "Cripto principal",
        "ticker": "ETH",
        "color": "#8b5cf6",
        "expected_return": 0.22,
        "volatility": 0.75,
        "risk_level": "alto",
        "description": "Segunda cripto por capitalización. Base de contratos inteligentes y apps descentralizadas. Más volatilidad que Bitcoin.",
        "currency": "USD",
        "market": "Exchanges",
        "simple_desc": "Ethereum: la plataforma de apps descentralizadas más usada",
    },
    {
        "id": "usdt",
        "name": "USDT / Stablecoin",
        "category": "Cripto",
        "sub": "Stablecoin",
        "ticker": "USDT",
        "color": "#22c55e",
        "expected_return": 0.05,
        "volatility": 0.01,
        "risk_level": "muy bajo",
        "description": "Moneda digital atada al dólar. Vale siempre cerca de 1 USD. No sube ni baja de precio, pero permite estar en dólares dentro de exchanges.",
        "currency": "USD",
        "market": "Exchanges",
        "simple_desc": "Dólar digital estable, sin riesgo de precio",
    },
]

# ─── Índice por ID ─────────────────────────────────────────────────────────────
ASSET_INDEX = {a["id"]: a for a in ASSET_UNIVERSE}


# ─── Plantillas de cartera por perfil ─────────────────────────────────────────
PORTFOLIO_TEMPLATES = {
    "conservador": {
        "expected_cagr": 0.065,
        "expected_volatility": 0.06,
        "description": "Prioriza la seguridad y la liquidez. Ideal para alguien que no quiere arriesgar su capital.",
        "summary": "Tu cartera está pensada para mantener el valor de tu plata con el menor riesgo posible. La mayor parte está en pesos con buena liquidez, un poco en dólares para protegerte de la devaluación, y algo en inversiones seguras en USD.",
        "allocations": {
            "money_market":   0.18,
            "plazo_fijo":     0.12,
            "fci_t0":         0.10,
            "cer_bond":       0.10,
            "lecap":          0.10,
            "mep":            0.12,
            "on_corp":        0.08,
            "on_pampa":       0.08,
            "spy":            0.05,
            "gld":            0.04,
            "iau":            0.03,
        },
    },
    "moderado": {
        "expected_cagr": 0.105,
        "expected_volatility": 0.15,
        "description": "Equilibrio entre crecimiento y protección. Mezcla inversiones seguras con algo de riesgo controlado.",
        "summary": "Tu cartera combina estabilidad con crecimiento. Tenés una base sólida en activos seguros y, encima de eso, inversiones en empresas y bonos que pueden darte mejor rendimiento a mediano plazo.",
        "allocations": {
            "spy":            0.15,
            "vti":            0.08,
            "qqq":            0.07,
            "msft":           0.06,
            "aapl":           0.05,
            "brk":            0.05,
            "on_corp":        0.07,
            "on_pampa":       0.05,
            "al30":           0.07,
            "mep":            0.08,
            "lecap":          0.07,
            "money_market":   0.08,
            "cer_bond":       0.06,
            "gld":            0.06,
        },
    },
    "agresivo": {
        "expected_cagr": 0.170,
        "expected_volatility": 0.30,
        "description": "Maximiza el crecimiento a largo plazo, aceptando que puede haber caídas fuertes en el camino.",
        "summary": "Tu cartera apunta al máximo crecimiento. Estás dispuesto a ver caídas fuertes a corto plazo a cambio de mejores resultados a largo plazo. Tenés exposición a tecnología, mercados globales, acciones argentinas y algo de cripto.",
        "allocations": {
            "qqq":            0.12,
            "spy":            0.08,
            "nvda":           0.07,
            "meli":           0.06,
            "meta":           0.05,
            "msft":           0.05,
            "amzn":           0.04,
            "tsla":           0.04,
            "ypf":            0.06,
            "vist":           0.04,
            "galicia":        0.04,
            "pampa":          0.03,
            "al30":           0.06,
            "gd30":           0.04,
            "mep":            0.05,
            "btc":            0.07,
            "eth":            0.03,
            "money_market":   0.03,
            "on_tecpetrol":   0.04,
        },
    },
}


def _adjust_for_horizon(allocations: dict, horizon: int, risk: str) -> dict:
    """Ajusta ponderaciones según horizonte temporal."""
    adj = dict(allocations)

    if horizon <= 2:
        # Corto plazo: más liquidez, menos equity volátil
        risky = ["ypf", "galicia", "pampa", "teco2", "qqq", "meli", "nvda", "tsla", "btc", "eth"]
        safe  = ["money_market", "plazo_fijo", "fci_t0", "mep", "lecap"]
        rescued = 0.0
        for k in risky:
            if k in adj and adj[k] > 0.04:
                cut = adj[k] * 0.4
                adj[k] -= cut
                rescued += cut
        # Repartir a liquidez
        for k in safe:
            if k in adj:
                adj[k] += rescued / len([s for s in safe if s in adj])
                break

    elif horizon >= 8:
        # Largo plazo: más equity, menos cash
        for k in ["money_market", "plazo_fijo", "fci_t0", "lecap"]:
            if k in adj:
                freed = adj[k] * 0.4
                adj[k] -= freed
                for g in ["spy", "qqq", "meli"]:
                    if g in adj:
                        adj[g] += freed / len([x for x in ["spy", "qqq", "meli"] if x in adj])
                        break

    total = sum(adj.values())
    return {k: v / total for k, v in adj.items() if v > 0.005}


def _adjust_for_emergency(allocations: dict, has_emergency: bool) -> dict:
    """Si no tiene fondo de emergencia, aumenta liquidez."""
    if has_emergency:
        return allocations
    adj = dict(allocations)
    boost = 0.06
    liquid = "money_market" if "money_market" in adj else "plazo_fijo"
    if liquid in adj:
        adj[liquid] += boost
        # Recortar proporcional al resto
        rest_total = sum(v for k, v in adj.items() if k != liquid)
        for k in adj:
            if k != liquid:
                adj[k] *= (1 - boost) / (rest_total / sum(adj.values()))
    total = sum(adj.values())
    return {k: v / total for k, v in adj.items()}


def build_portfolio(profile: dict) -> dict:
    """Construye la cartera personalizada según el perfil del inversor."""
    risk     = profile["risk_profile"]
    template = PORTFOLIO_TEMPLATES[risk]
    allocs   = dict(template["allocations"])

    horizon       = profile.get("horizon", 5)
    allocs        = _adjust_for_horizon(allocs, horizon, risk)

    has_emergency = ("más de" in profile.get("emergency_fund", "").lower()
                     or "6 meses" in profile.get("emergency_fund", "").lower())
    allocs        = _adjust_for_emergency(allocs, has_emergency)

    # Construir posiciones
    positions = []
    for asset_id, weight in allocs.items():
        if asset_id in ASSET_INDEX and weight > 0.005:
            asset          = dict(ASSET_INDEX[asset_id])
            asset["weight"] = round(weight, 4)
            positions.append(asset)

    positions.sort(key=lambda x: x["weight"], reverse=True)

    # Métricas
    expected_cagr = sum(p["weight"] * p["expected_return"] for p in positions)
    expected_vol  = sum(p["weight"] * p["volatility"]      for p in positions)

    category_exposure: Dict[str, float] = {}
    sector_exposure:   Dict[str, float] = {}
    currency_exposure: Dict[str, float] = {}

    for p in positions:
        category_exposure[p["category"]] = category_exposure.get(p["category"], 0) + p["weight"]
        sector_exposure[p["sub"]]        = sector_exposure.get(p["sub"], 0)        + p["weight"]
        currency_exposure[p["currency"]] = currency_exposure.get(p["currency"], 0) + p["weight"]

    # % en pesos vs USD
    pesos_pct = sum(p["weight"] for p in positions if p["currency"] == "ARS") * 100
    usd_pct   = 100 - pesos_pct

    # Nivel de diversificación
    n = len(positions)
    if n >= 10:
        diversification = "alta"
    elif n >= 6:
        diversification = "media"
    else:
        diversification = "baja"

    return {
        "risk_profile":        risk,
        "positions":           positions,
        "expected_cagr":       round(expected_cagr, 4),
        "expected_volatility": round(expected_vol, 4),
        "category_exposure":   category_exposure,
        "sector_exposure":     sector_exposure,
        "currency_exposure":   currency_exposure,
        "description":         template["description"],
        "summary":             template["summary"],
        "pesos_pct":           round(pesos_pct, 1),
        "usd_pct":             round(usd_pct, 1),
        "diversification":     diversification,
        "profile":             profile,
    }
