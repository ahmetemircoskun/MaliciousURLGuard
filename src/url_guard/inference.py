"""Prediction helpers used by Streamlit and tests."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np

from .config import BRANDS, DEFAULT_THRESHOLD
from .features import extract_features
from .url_tools import canonicalize_url


@dataclass(frozen=True)
class Prediction:
    raw_url: str
    canonical_url: str
    label: int
    probability_malicious: float
    probability_safe: float
    threshold: float
    features: dict[str, float]
    notes: list[str]


def load_artifacts(base_dir: str | Path):
    base = Path(base_dir)
    payload = joblib.load(base / "models" / "best_model.joblib")
    scaler = joblib.load(base / "models" / "scaler.joblib")
    return payload, scaler


def _rule_adjustment(raw_url: str, canonical_url: str, features: dict[str, float], model_prob: float) -> tuple[float, list[str]]:
    notes: list[str] = []
    prob = float(model_prob)
    parts = canonicalize_url(canonical_url)

    if features.get("is_valid_url", 0) == 0:
        return 0.99, ["URL teknik olarak geçerli görünmüyor."]

    if features.get("brand_in_subdomain", 0) or features.get("brand_in_path", 0):
        prob = max(prob, 0.88)
        notes.append("Marka adı gerçek alan adı dışında kullanılmış.")
    elif features.get("brand_in_url", 0):
        prob = max(prob, 0.76)
        notes.append("Marka adı URL içinde geçiyor ama ana alan adı o marka değil.")

    if features.get("has_ip", 0):
        prob = max(prob, 0.74)
        notes.append("Alan adı yerine IP adresi kullanılmış.")

    if features.get("has_at_symbol", 0):
        prob = max(prob, 0.78)
        notes.append("@ işareti host bilgisini yanıltıcı gösterebilir.")

    first_party_brand = parts.domain_core in BRANDS
    low_risk_brand_root = (
        first_party_brand
        and features.get("has_trusted_tld", 0) == 1
        and features.get("brand_in_url", 0) == 0
        and features.get("brand_in_subdomain", 0) == 0
        and features.get("brand_in_path", 0) == 0
        and features.get("has_ip", 0) == 0
        and features.get("has_suspicious_tld", 0) == 0
        and features.get("is_shortened", 0) == 0
        and features.get("num_subdomains", 0) <= 2
    )
    if low_risk_brand_root:
        prob = min(prob, 0.18)
        notes.append("Bilinen markanın kendi ana alan adı gibi görünüyor.")

    if raw_url.strip().lower().startswith("https://") and prob < 0.75:
        prob *= 0.96

    return max(0.0, min(1.0, prob)), notes


def predict_url(url: str, payload: dict, scaler) -> Prediction:
    raw = str(url).strip()
    parts = canonicalize_url(raw)
    features = extract_features(raw)
    feature_cols = payload["feature_cols"]
    threshold = float(payload.get("threshold", DEFAULT_THRESHOLD))
    x = np.array([[features.get(col, 0.0) for col in feature_cols]])
    model_prob = float(payload["model"].predict_proba(scaler.transform(x))[0][1])
    prob_mal, notes = _rule_adjustment(raw, parts.canonical, features, model_prob)
    label = int(prob_mal >= threshold)
    return Prediction(raw, parts.canonical, label, prob_mal, 1.0 - prob_mal, threshold, features, notes)

