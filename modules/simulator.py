"""
Módulo de simulación de cartera
Implementa simulación de trayectoria con escenarios: optimista, base y pesimista.
También incluye Monte Carlo simplificado.
"""

import numpy as np
from typing import Dict, Any


def simulate_portfolio(
    portfolio: dict,
    years: int = 5,
    initial_capital: float = 10_000,
    custom_cagr: float | None = None,
    custom_vol: float | None = None,
    n_simulations: int = 200,
    seed: int = 42,
) -> Dict[str, Any]:
    """
    Simula la evolución del portafolio a lo largo del tiempo.

    Retorna:
        - scenarios: dict con arrays de valores para 'base', 'optimista', 'pesimista'
        - monte_carlo: percentiles de las simulaciones MC
        - years_axis: eje temporal
        - summary: estadísticas clave
    """
    rng = np.random.default_rng(seed)

    cagr = custom_cagr if custom_cagr is not None else portfolio["expected_cagr"]
    vol  = custom_vol  if custom_vol  is not None else portfolio["expected_volatility"]

    # Convertir horizonte a puntos mensuales
    months = years * 12
    t = np.linspace(0, years, months + 1)
    dt = 1 / 12  # paso mensual

    # ── Escenarios deterministas ──────────────────────────────────────────────
    # Base: cagr exacto
    base = initial_capital * np.exp(cagr * t)

    # Optimista: cagr + 0.5σ anualizado extra
    optimistic_cagr = cagr + vol * 0.5
    optimista = initial_capital * np.exp(optimistic_cagr * t)

    # Pesimista: cagr - 0.5σ anualizado menos
    pessimistic_cagr = max(cagr - vol * 0.7, -0.30)
    pesimista = initial_capital * np.exp(pessimistic_cagr * t)

    # ── Monte Carlo ────────────────────────────────────────────────────────────
    mu  = cagr - 0.5 * vol ** 2
    sig = vol

    paths = np.zeros((n_simulations, months + 1))
    paths[:, 0] = initial_capital

    for s in range(n_simulations):
        z = rng.standard_normal(months)
        log_returns = mu * dt + sig * np.sqrt(dt) * z
        paths[s, 1:] = initial_capital * np.exp(np.cumsum(log_returns))

    p10 = np.percentile(paths, 10, axis=0)
    p25 = np.percentile(paths, 25, axis=0)
    p50 = np.percentile(paths, 50, axis=0)
    p75 = np.percentile(paths, 75, axis=0)
    p90 = np.percentile(paths, 90, axis=0)

    # ── Métricas resumen ───────────────────────────────────────────────────────
    prob_positive = float(np.mean(paths[:, -1] > initial_capital))
    prob_double   = float(np.mean(paths[:, -1] > initial_capital * 2))
    prob_loss_20  = float(np.mean(paths[:, -1] < initial_capital * 0.80))
    median_final  = float(np.median(paths[:, -1]))
    mean_final    = float(np.mean(paths[:, -1]))
    worst_final   = float(np.percentile(paths[:, -1], 5))
    best_final    = float(np.percentile(paths[:, -1], 95))

    return {
        "scenarios": {
            "base":      base.tolist(),
            "optimista": optimista.tolist(),
            "pesimista": pesimista.tolist(),
        },
        "monte_carlo": {
            "p10": p10.tolist(),
            "p25": p25.tolist(),
            "p50": p50.tolist(),
            "p75": p75.tolist(),
            "p90": p90.tolist(),
        },
        "years_axis": t.tolist(),
        "summary": {
            "prob_positive": prob_positive,
            "prob_double":   prob_double,
            "prob_loss_20":  prob_loss_20,
            "median_final":  median_final,
            "mean_final":    mean_final,
            "worst_final":   worst_final,
            "best_final":    best_final,
            "cagr_used":     cagr,
            "vol_used":      vol,
        },
        "n_simulations": n_simulations,
        "years":         years,
        "initial_capital": initial_capital,
    }
