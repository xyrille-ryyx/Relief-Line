from flask import Blueprint, render_template, session, redirect, url_for
from app import mysql
import importlib
import jinja2
import numbers
import numpy as np
import math

prediction_bp = Blueprint("prediction", __name__)


def _sanitize_for_json(obj):
    """Recursively convert objects to JSON-serializable native types.

    - Replace Jinja `Undefined` with None
    - Convert numpy scalars/arrays to Python numbers
    - Convert non-serializable objects to strings as a last resort
    """
    if isinstance(obj, jinja2.Undefined):
        return None
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {str(k): _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize_for_json(v) for v in obj]
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return [_sanitize_for_json(v) for v in obj.tolist()]
    if isinstance(obj, numbers.Number):
        # guard against NaN/Inf which json can't represent
        if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
            return None
        return obj
    if isinstance(obj, (str, bool)):
        return obj
    try:
        # last-ditch: attempt to convert to a python primitive
        return float(obj) if hasattr(obj, '__float__') else str(obj)
    except Exception:
        return str(obj)

# Demand level thresholds (food packs), per city/municipality total.
# Mirrors the "Demand Level Guide" already defined in prediction.html.
def classify_demand_level(total_projected: int) -> str:
    if total_projected > 6000:
        return "critical"
    if total_projected >= 4000:
        return "high"
    if total_projected >= 2500:
        return "moderate"
    return "low"


DEMAND_LABELS = {
    "critical": "Critical Demand",
    "high": "High Demand",
    "moderate": "Moderate Demand",
    "low": "Low Demand",
}


@prediction_bp.route("/prediction")
def prediction():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT barangay_id, barangay_name, city_municipality, population,
               num_households, poverty_incidence, disaster_risk_index,
               past_calamity_freq
        FROM barangays
        ORDER BY city_municipality, barangay_name
    """)
    columns = [desc[0] for desc in cur.description]
    rows = [dict(zip(columns, row)) for row in cur.fetchall()]

    # historical_allocation is required by the model but lives in
    # allocation_records, not barangays. Pull the most recent allocation
    # per barangay (falls back to 0 if a barangay has no prior records).
    cur.execute("""
        SELECT ar.barangay_id, ar.historical_allocation
        FROM allocation_records ar
        INNER JOIN (
            SELECT barangay_id, MAX(allocation_date) AS latest_date
            FROM allocation_records
            GROUP BY barangay_id
        ) latest
        ON ar.barangay_id = latest.barangay_id
        AND ar.allocation_date = latest.latest_date
    """)
    historical_map = {bid: hist for bid, hist in cur.fetchall()}
    cur.close()

    for row in rows:
        row["historical_allocation"] = historical_map.get(row["barangay_id"], 0)

    # Run the Linear Regression model for every barangay. Import lazily
    try:
        predict_mod = importlib.import_module('app.ml.predict')
        predict_for_barangays = getattr(predict_mod, 'predict_for_barangays')
        predicted_rows = predict_for_barangays(rows)
    except Exception:
        # If the ML module is unavailable or fails to load, fall back to
        # a safe default (zero predictions) so the UI can still render.
        predicted_rows = []
        for row in rows:
            enriched = dict(row)
            enriched['predicted_quantity'] = 0
            predicted_rows.append(enriched)

    # Save each prediction to prediction_logs for audit/traceability
    _log_predictions(predicted_rows)

    # Aggregate per city/municipality for the summary cards and chart
    city_groups = {}
    for r in predicted_rows:
        city = r["city_municipality"]
        city_groups.setdefault(city, {
            "area": city,
            "barangays": 0,
            "projected": 0,
            "historical": 0,
        })
        city_groups[city]["barangays"] += 1
        city_groups[city]["projected"] += r["predicted_quantity"]
        city_groups[city]["historical"] += r["historical_allocation"]

    forecast_data = []
    for city, agg in city_groups.items():
        diff = agg["projected"] - agg["historical"]
        diff_pct = round((diff / agg["historical"]) * 100, 1) if agg["historical"] > 0 else 0
        level = classify_demand_level(agg["projected"])
        forecast_data.append({
            "id": city.lower().replace(" ", ""),
            "area": city,
            "barangays": agg["barangays"],
            "projected": agg["projected"],
            "historical": agg["historical"],
            "diff": diff,
            "diffPct": diff_pct,
            "level": level,
            "levelLabel": DEMAND_LABELS[level],
        })

    return render_template(
        "prediction.html",
        forecast_data=_sanitize_for_json(forecast_data),
        barangay_predictions=_sanitize_for_json(predicted_rows),
    )


def _log_predictions(predicted_rows: list[dict]):
    """Writes each prediction to prediction_logs for traceability."""
    import json
    cur = mysql.connection.cursor()
    for r in predicted_rows:
        snapshot = {
            "population": r["population"],
            "num_households": r["num_households"],
            "poverty_incidence": float(r["poverty_incidence"]),
            "disaster_risk_index": float(r["disaster_risk_index"]),
            "past_calamity_freq": r["past_calamity_freq"],
            "historical_allocation": r["historical_allocation"],
        }
        cur.execute("""
            INSERT INTO prediction_logs (barangay_id, predicted_quantity, input_snapshot, model_version)
            VALUES (%s, %s, %s, %s)
        """, (r["barangay_id"], r["predicted_quantity"], json.dumps(snapshot), "v1.0"))
    mysql.connection.commit()
    cur.close()