# FinanzasIA — Asesor Financiero Inteligente 📊

Aplicación web de asesoría financiera personal con inteligencia artificial para el mercado argentino.

## Características

- 🎯 **Perfil de riesgo adaptativo** — Cuestionario de 8 preguntas para detectar perfil conservador, moderado o agresivo
- 💼 **Cartera teórica diversificada** — Acciones locales, CEDEARs, ETFs, bonos, dólar MEP y cash
- 🤖 **Asesoría IA con Claude** — Justificación de activos, alertas de sobreexposición y consejos de rebalanceo
- 📈 **Simulación Monte Carlo** — Evolución proyectada con escenarios optimista/base/pesimista
- ⚙️ **Supuestos ajustables** — Modificá retorno y volatilidad para ver distintos escenarios

## Stack Tecnológico

- **Frontend**: Streamlit (UI moderna con CSS personalizado)
- **Backend**: Python 3.11+
- **IA**: Anthropic Claude API (claude-sonnet-4)
- **Gráficos**: Plotly
- **Simulación**: NumPy (Monte Carlo)

## Instalación

```bash
# 1. Clonar o copiar el proyecto
cd finanzas_app

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar API key de Anthropic
export ANTHROPIC_API_KEY="tu-api-key-aqui"
# En Windows: set ANTHROPIC_API_KEY=tu-api-key-aqui

# 5. Ejecutar la aplicación
streamlit run app.py
```

## Configuración de API Key

Obtené tu API key en: https://console.anthropic.com/

Podés configurarla de tres formas:
1. Variable de entorno: `export ANTHROPIC_API_KEY="sk-ant-..."`
2. Archivo `.env` (requiere python-dotenv)
3. Secrets de Streamlit Cloud: `.streamlit/secrets.toml`

```toml
# .streamlit/secrets.toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

## Estructura del Proyecto

```
finanzas_app/
├── app.py                    # Punto de entrada principal
├── requirements.txt          # Dependencias
├── README.md                 # Este archivo
└── modules/
    ├── __init__.py
    ├── ui_config.py          # CSS personalizado y componentes de UI
    ├── profiler.py           # Cuestionario de perfil de riesgo
    ├── portfolio.py          # Motor de construcción de carteras
    ├── simulator.py          # Simulación Monte Carlo
    ├── charts.py             # Visualizaciones Plotly
    └── ai_advisor.py         # Integración con Claude AI
```

## Activos Incluidos

| Categoría      | Activos |
|----------------|---------|
| Acciones ARG   | YPF (YPFD), Banco Galicia (GGAL) |
| CEDEARs        | MercadoLibre (MELI), Apple (AAPL) |
| ETFs           | S&P 500 (SPY), Nasdaq 100 (QQQ), Emergentes (EEM) |
| Bonos          | AL30, LECAPs, Obligaciones Negociables |
| Dólar MEP      | USD MEP via BYMA |
| Cash           | Fondos Money Market |

## Disclaimer

⚠️ Esta aplicación es únicamente para fines educativos y no constituye asesoramiento financiero profesional. Consultá siempre con un asesor financiero habilitado (CNV/CAFCI) antes de tomar decisiones de inversión.

## Licencia

MIT License — Libre uso educativo y personal.
