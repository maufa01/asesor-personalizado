"""
Módulo de asesoría IA
Usa la API de Anthropic (Claude) para generar:
  - Justificación de la cartera recomendada
  - Alertas de sobreexposición sectorial
  - Sugerencias de rebalanceo
  - Consejos financieros personalizados
"""

import os
import json
import anthropic
from typing import Dict, Any, List


def _build_portfolio_summary(portfolio: dict, profile: dict) -> str:
    """Construye un resumen estructurado de cartera y perfil para el prompt."""
    positions_txt = "\n".join(
        f"  - {p['name']} ({p['ticker']}): {p['weight']*100:.1f}% "
        f"[Ret. esperado: {p['expected_return']*100:.1f}%, "
        f"Volatilidad: {p['volatility']*100:.1f}%, "
        f"Categoría: {p['category']}]"
        for p in portfolio["positions"]
    )
    cat_txt = "\n".join(
        f"  - {cat}: {w*100:.1f}%" for cat, w in portfolio["category_exposure"].items()
    )
    sector_txt = "\n".join(
        f"  - {sec}: {w*100:.1f}%" for sec, w in portfolio["sector_exposure"].items()
    )
    cur_txt = "\n".join(
        f"  - {cur}: {w*100:.1f}%" for cur, w in portfolio["currency_exposure"].items()
    )

    return f"""
PERFIL DEL INVERSOR:
- Perfil de riesgo: {profile['risk_profile'].upper()}
- Score de riesgo: {profile['risk_score']}/{profile['risk_max']}
- Horizonte: {profile['horizon']} años
- Capital a invertir: USD {profile['capital']:,.0f}
- Objetivo: {profile['objective']}
- Estabilidad de ingresos: {profile['income_stability']}
- Tolerancia a pérdidas: {profile['loss_tolerance']}
- Experiencia: {profile['experience']}
- Fondo de emergencia: {profile['emergency_fund']}

CARTERA RECOMENDADA:
{positions_txt}

RETORNO ESPERADO ANUAL: {portfolio['expected_cagr']*100:.1f}%
VOLATILIDAD ESPERADA: {portfolio['expected_volatility']*100:.1f}%

EXPOSICIÓN POR CATEGORÍA:
{cat_txt}

EXPOSICIÓN POR SECTOR:
{sector_txt}

EXPOSICIÓN POR MONEDA:
{cur_txt}
"""


def get_ai_analysis(profile: dict, portfolio: dict) -> Dict[str, Any]:
    """
    Llama a la API de Anthropic para obtener análisis completo de la cartera.
    Retorna un dict con justificación, alertas, rebalanceo y consejos.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    portfolio_summary = _build_portfolio_summary(portfolio, profile)

    system_prompt = """Sos un asesor financiero experto en mercados argentinos e internacionales, 
especializado en inversiones para individuos. Tu tarea es analizar carteras de inversión y 
brindar análisis claros, prácticos y educativos en español rioplatense (argentino).

Contexto: Argentina tiene inflación alta, inestabilidad cambiaria, acceso a dólares MEP/CCL, 
y un mercado local (BYMA) con CEDEARs, bonos soberanos y acciones locales. Los inversores 
argentinos tienen consideraciones especiales respecto al tipo de cambio y la cobertura inflacionaria.

Tus respuestas deben ser:
- Claras y educativas (sin jerga excesiva)
- Específicas al contexto argentino
- Honestas sobre los riesgos
- En español rioplatense (usá "vos", "acá", etc.)
- Estructuradas con párrafos y listas cuando corresponda

IMPORTANTE: Responder SIEMPRE en formato JSON válido con exactamente estas claves:
{
  "justification": "...",
  "alerts": [
    {"title": "...", "message": "...", "severity": "high|medium|low"}
  ],
  "rebalancing": "...",
  "tips": "..."
}"""

    user_prompt = f"""Analizá la siguiente cartera de inversión y generá un análisis completo:

{portfolio_summary}

Por favor respondé con el JSON solicitado que incluya:

1. "justification": Una explicación detallada (4-6 párrafos) de por qué se recomienda cada tipo 
   de activo, cómo encajan con el perfil del inversor, y cuáles son las ventajas de esta diversificación.
   Explicá por qué los CEDEARs son útiles para cobertura cambiaria, por qué se incluyen bonos, etc.

2. "alerts": Una lista de 2-4 alertas sobre posibles riesgos, sobreexposición sectorial o 
   concentración excesiva. Cada alerta debe tener título, mensaje explicativo y severidad (high/medium/low).
   Considerá: concentración en sectores, riesgo soberano argentino, exposición cambiaria, liquidez.

3. "rebalancing": Consejos concretos de cuándo y cómo rebalancear esta cartera (3-4 párrafos).
   Incluí señales de mercado que deberían trigger un rebalanceo, y cómo ajustar en diferentes 
   escenarios macroeconómicos para Argentina.

4. "tips": 4-5 consejos prácticos adicionales para este inversor específico basados en su perfil,
   horizonte y capital disponible. Incluí sugerencias sobre plataformas, herramientas de seguimiento,
   y hábitos financieros recomendados."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        raw_text = response.content[0].text.strip()

        # Limpiar markdown si viene envuelto en ```json
        if raw_text.startswith("```"):
            lines = raw_text.split("\n")
            raw_text = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

        analysis = json.loads(raw_text)

        # Asegurar que tiene todas las claves esperadas
        defaults = {
            "justification": "Análisis no disponible.",
            "alerts": [],
            "rebalancing": "Sugerencias no disponibles.",
            "tips": "Consejos no disponibles.",
        }
        for k, v in defaults.items():
            if k not in analysis:
                analysis[k] = v

        return analysis

    except json.JSONDecodeError:
        # Si el JSON falla, retornar la respuesta como texto en justification
        return {
            "justification": raw_text,
            "alerts": [],
            "rebalancing": "Error al parsear la respuesta estructurada.",
            "tips": "Por favor, regenerá el análisis.",
        }
    except Exception as e:
        return {
            "justification": f"Error al conectar con la IA: {str(e)}\n\nAsegurate de configurar la variable de entorno ANTHROPIC_API_KEY.",
            "alerts": [
                {
                    "title": "Error de configuración",
                    "message": "No se pudo conectar con la API de IA. Verificá tu API key.",
                    "severity": "high",
                }
            ],
            "rebalancing": "No disponible por error de conexión.",
            "tips": "Configurá la variable ANTHROPIC_API_KEY para usar el asesor IA.",
        }


def get_rebalancing_advice(portfolio: dict, profile: dict) -> str:
    """
    Función auxiliar para obtener solo consejos de rebalanceo.
    Útil para llamadas rápidas sin análisis completo.
    """
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

    positions_txt = ", ".join(
        f"{p['name']} ({p['weight']*100:.0f}%)" for p in portfolio["positions"][:5]
    )

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{
                "role": "user",
                "content": f"""En 2-3 párrafos cortos y en español argentino, 
                dame consejos específicos de rebalanceo para una cartera {profile['risk_profile']} 
                con horizonte de {profile['horizon']} años que incluye: {positions_txt}.
                Considerá el contexto macroeconómico de Argentina.""",
            }],
        )
        return response.content[0].text
    except Exception as e:
        return f"Error: {e}"
