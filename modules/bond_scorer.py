"""
Scorer de bonos argentinos.
Fuentes de datos: rava.com (primaria) → ambito.com (backup) → static fallback.

Uso offline:
    python -m modules.bond_scorer

Genera bond_scores.json con scores 0-100 por instrumento de renta fija.
"""

import json
import time
import re
from pathlib import Path
from datetime import date

import requests

BOND_SCORES_PATH = Path(__file__).parent.parent / "bond_scores.json"
REQUEST_DELAY = 1.5

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/html, */*",
}

# ─── Definición de bonos ──────────────────────────────────────────────────────
# tir_est   : rendimiento estimado (% anual en la moneda del bono)
# duration_est: duración modificada estimada (años)
# paridad_est : precio como % del valor par
# quality_pts : puntaje fijo de calidad crediticia (0-25)
# vol_est_m   : volumen diario estimado en millones de ARS
# ticker_rava : símbolo en rava.com / BYMA

BOND_DEFS = {
    "al30": {
        "label":        "AL30 – Bono Global USD Ley Argentina",
        "type":         "soberano_usd",
        "ticker_rava":  "AL30",
        "ticker_ambito": "AL30",
        "tir_est":      8.5,
        "duration_est": 3.5,
        "paridad_est":  47.0,
        "quality_pts":  16,
        "vol_est_m":    4.0,
    },
    "gd30": {
        "label":        "GD30 – Bono Global USD Ley Nueva York",
        "type":         "soberano_usd",
        "ticker_rava":  "GD30",
        "ticker_ambito": "GD30",
        "tir_est":      8.5,
        "duration_est": 4.0,
        "paridad_est":  47.0,
        "quality_pts":  17,
        "vol_est_m":    6.0,
    },
    "lecap": {
        "label":        "LECAPs – Letras Capitalizables del Tesoro",
        "type":         "lecap",
        "ticker_rava":  "S31M26",
        "ticker_ambito": "S31M26",
        "tir_est":      62.0,
        "duration_est": 0.25,
        "paridad_est":  99.5,
        "quality_pts":  18,
        "vol_est_m":    10.0,
    },
    "cer_bond": {
        "label":        "Bono CER – Ajuste por Inflación",
        "type":         "cer",
        "ticker_rava":  "TZXD5",
        "ticker_ambito": "TZXD5",
        "tir_est":      5.0,
        "duration_est": 1.5,
        "paridad_est":  96.0,
        "quality_pts":  17,
        "vol_est_m":    2.5,
    },
    "on_ypf": {
        "label":        "ON YPF USD",
        "type":         "on_corp",
        "ticker_rava":  "YPFDS",
        "ticker_ambito": "YPFDS",
        "tir_est":      9.0,
        "duration_est": 2.5,
        "paridad_est":  98.0,
        "quality_pts":  22,
        "vol_est_m":    2.0,
    },
    "on_corp": {
        "label":        "ONs Corporativas Mix (Pampa / Arcor / MELI)",
        "type":         "on_corp",
        "ticker_rava":  "PTSTO",
        "ticker_ambito": "PTSTO",
        "tir_est":      8.5,
        "duration_est": 2.0,
        "paridad_est":  100.0,
        "quality_pts":  20,
        "vol_est_m":    2.0,
    },
    "on_pampa": {
        "label":        "ON Pampa Energía USD",
        "type":         "on_corp",
        "ticker_rava":  "PTSTO",
        "ticker_ambito": "PTSTO",
        "tir_est":      8.0,
        "duration_est": 2.0,
        "paridad_est":  100.0,
        "quality_pts":  22,
        "vol_est_m":    1.5,
    },
    "on_tecpetrol": {
        "label":        "ON Tecpetrol USD",
        "type":         "on_corp",
        "ticker_rava":  "TCCUD",
        "ticker_ambito": "TCCUD",
        "tir_est":      8.0,
        "duration_est": 2.5,
        "paridad_est":  99.0,
        "quality_pts":  22,
        "vol_est_m":    1.0,
    },
}

# ─── Fetchers ─────────────────────────────────────────────────────────────────

def _fetch_rava(ticker: str) -> dict | None:
    """
    Intenta obtener precio y volumen desde rava.com.
    Devuelve {paridad, vol_m} o None si falla.
    """
    try:
        url = f"https://www.rava.com/api/cotizaciones.php?asset={ticker}&ReduccionDatos=0"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()

        if isinstance(data, list) and data:
            row = data[0]
        elif isinstance(data, dict):
            row = data
        else:
            return None

        precio = (
            row.get("Ultimo") or row.get("ultimo") or
            row.get("PrecioUltimo") or row.get("precioUltimo")
        )
        volumen = (
            row.get("Volumen") or row.get("volumen") or
            row.get("VolumenNominal") or row.get("volumenNominal") or 0
        )

        if precio is None:
            return None

        precio = float(str(precio).replace(",", "."))
        volumen = float(str(volumen).replace(",", "").replace(".", "")) if volumen else 0

        return {
            "paridad": precio,
            "vol_m": volumen / 1_000_000,
        }
    except Exception:
        return None


def _fetch_ambito(ticker: str) -> dict | None:
    """
    Backup: obtiene precio desde ambito.com.
    Devuelve {paridad, vol_m} o None si falla.
    """
    try:
        url = f"https://mercados.ambito.com/bonos/informacion-general/{ticker}"
        r = requests.get(url, headers=HEADERS, timeout=10)
        r.raise_for_status()
        data = r.json()

        precio_raw = (
            data.get("ultimo") or data.get("cierre") or
            data.get("apertura") or data.get("Ultimo")
        )
        volumen_raw = data.get("volumen") or data.get("Volumen") or 0

        if precio_raw is None:
            return None

        precio = float(str(precio_raw).replace(",", "."))
        volumen = float(re.sub(r"[^\d]", "", str(volumen_raw))) if volumen_raw else 0

        return {
            "paridad": precio,
            "vol_m": volumen / 1_000_000,
        }
    except Exception:
        return None


def _fetch_live(ticker: str) -> dict | None:
    live = _fetch_rava(ticker)
    if not live:
        live = _fetch_ambito(ticker)
    return live


# ─── Scoring ──────────────────────────────────────────────────────────────────
# 5 bloques: Rendimiento 35 + Duration 20 + Calidad 25 + Paridad 10 + Liquidez 10

def _score_rendimiento(tir: float, bond_type: str) -> int:
    """35 pts. Mayor rendimiento = mejor, con umbrales por tipo."""
    max_pts = 35
    if bond_type in ("soberano_usd", "on_corp"):
        exc, bue, neu = 10.0, 8.0, 6.0
    elif bond_type == "cer":
        exc, bue, neu = 8.0, 5.0, 2.0
    elif bond_type == "lecap":
        exc, bue, neu = 70.0, 55.0, 45.0
    else:
        exc, bue, neu = 9.0, 7.0, 5.0

    if tir >= exc:   return max_pts
    elif tir >= bue: return round(max_pts * 0.75)
    elif tir >= neu: return round(max_pts * 0.45)
    else:            return round(max_pts * 0.10)


def _score_duration(duration_years: float) -> int:
    """20 pts. Menor duración = menor riesgo de tasa = mejor."""
    max_pts = 20
    if duration_years <= 0.5:  return max_pts
    elif duration_years <= 1.0: return round(max_pts * 0.75)
    elif duration_years <= 2.0: return round(max_pts * 0.45)
    else:                       return round(max_pts * 0.10)


def _score_paridad(paridad: float) -> int:
    """10 pts. Bajo la par = potencial de ganancia de capital = mejor."""
    max_pts = 10
    if paridad < 70:    return max_pts
    elif paridad < 85:  return round(max_pts * 0.80)
    elif paridad < 100: return round(max_pts * 0.50)
    else:               return round(max_pts * 0.20)


def _score_liquidez(vol_m: float) -> int:
    """10 pts. Volumen diario en millones de ARS."""
    max_pts = 10
    if vol_m >= 10.0:  return max_pts
    elif vol_m >= 3.0: return round(max_pts * 0.80)
    elif vol_m >= 1.0: return round(max_pts * 0.50)
    else:              return round(max_pts * 0.20)


def _rating(score: int) -> str:
    if score >= 80:   return "STRONG BUY"
    elif score >= 65: return "BUY"
    elif score >= 50: return "HOLD"
    elif score >= 35: return "UNDERWEIGHT"
    else:             return "AVOID"


def score_bond(asset_id: str, live_data: dict | None = None) -> dict:
    """
    Calcula el score de un bono (0-100).
    TIR y duration usan estimaciones estáticas (actualizables en BOND_DEFS).
    Paridad y volumen se toman de live_data si está disponible.
    """
    defn = BOND_DEFS[asset_id]

    tir      = defn["tir_est"]
    duration = defn["duration_est"]
    paridad  = live_data["paridad"] if live_data and "paridad" in live_data else defn["paridad_est"]
    vol_m    = live_data["vol_m"]   if live_data and "vol_m"   in live_data else defn["vol_est_m"]

    pts_rend = _score_rendimiento(tir, defn["type"])
    pts_dur  = _score_duration(duration)
    pts_qual = defn["quality_pts"]
    pts_par  = _score_paridad(paridad)
    pts_liq  = _score_liquidez(vol_m)

    total = pts_rend + pts_dur + pts_qual + pts_par + pts_liq

    return {
        "score":     total,
        "rating":    _rating(total),
        "live":      live_data is not None,
        "label":     defn["label"],
        "breakdown": {
            "rendimiento": pts_rend,
            "duration":    pts_dur,
            "calidad":     pts_qual,
            "paridad":     pts_par,
            "liquidez":    pts_liq,
        },
        "inputs": {
            "tir":      tir,
            "duration": duration,
            "paridad":  paridad,
            "vol_m":    round(vol_m, 2),
        },
    }


# ─── Runner offline ───────────────────────────────────────────────────────────

def run_and_save(path: Path = BOND_SCORES_PATH) -> dict:
    """
    Puntúa todos los bonos, muestra resultados en consola y guarda bond_scores.json.
    """
    print(f"\n{'─'*60}")
    print(f"BOND SCORER — {date.today()}")
    print(f"{'─'*60}\n")

    results = {}

    for asset_id, defn in BOND_DEFS.items():
        ticker = defn.get("ticker_rava")
        live   = None

        if ticker:
            print(f"  Fetching {ticker} ({defn['label']})...")
            live = _fetch_live(ticker)
            time.sleep(REQUEST_DELAY)

        result = score_bond(asset_id, live)
        results[asset_id] = result

        src = "LIVE paridad+vol" if result["live"] else "STATIC fallback"
        print(
            f"  {asset_id:<15} {result['score']:>3}  {result['rating']:<12}  "
            f"TIR={result['inputs']['tir']}%  par={result['inputs']['paridad']}%  "
            f"({src})"
        )

    output = {
        "as_of":       str(date.today()),
        "bond_scores": results,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n{'─'*60}")
    print(f"Guardado en {path}")
    print(f"{'─'*60}\n")
    return results


def load_scores(path: Path = BOND_SCORES_PATH) -> dict:
    """
    Carga bond_scores.json y devuelve {asset_id: score_int}.
    Devuelve dict vacío si el archivo no existe o está corrupto.
    """
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        return {k: v["score"] for k, v in data.get("bond_scores", {}).items()}
    except Exception:
        return {}


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    run_and_save()
