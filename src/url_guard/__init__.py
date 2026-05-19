"""Shared package for URL cleaning, feature extraction, training, and inference."""

from .features import FEATURE_SCHEMA, extract_features
from .inference import Prediction, predict_url
from .url_tools import canonicalize_url

__all__ = [
    "FEATURE_SCHEMA",
    "Prediction",
    "canonicalize_url",
    "extract_features",
    "predict_url",
]
