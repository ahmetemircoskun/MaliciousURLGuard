"""Training entrypoint for the malicious URL model."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    PrecisionRecallDisplay,
    RocCurveDisplay,
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from .config import DEFAULT_THRESHOLD, RANDOM_STATE
from .data import clean_dataset
from .features import FEATURE_SCHEMA, extract_features


def build_feature_frame(urls: pd.Series) -> pd.DataFrame:
    return pd.DataFrame([extract_features(url) for url in urls], columns=FEATURE_SCHEMA)


def train_project(base_dir: str | os.PathLike[str]) -> dict[str, float]:
    base = Path(base_dir)
    raw_path = base / "data" / "raw" / "malicious_phish.csv"
    processed_dir = base / "data" / "processed"
    model_dir = base / "models"
    processed_dir.mkdir(parents=True, exist_ok=True)
    model_dir.mkdir(parents=True, exist_ok=True)

    cleaned = clean_dataset(str(raw_path))
    cleaned_path = processed_dir / "cleaned_dataset.csv"
    cleaned.to_csv(cleaned_path, index=False)

    X_df = build_feature_frame(cleaned["url"])
    y = cleaned["label"].astype(int).to_numpy()

    X_train_df, X_test_df, y_train, y_test = train_test_split(
        X_df, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train_df)
    X_test = scaler.transform(X_test_df)

    base_model = HistGradientBoostingClassifier(
        max_iter=420,
        learning_rate=0.045,
        max_leaf_nodes=45,
        min_samples_leaf=20,
        l2_regularization=0.15,
        early_stopping=True,
        validation_fraction=0.1,
        n_iter_no_change=18,
        random_state=RANDOM_STATE,
    )
    model = CalibratedClassifierCV(base_model, method="sigmoid", cv=3)
    model.fit(X_train, y_train)

    y_prob = model.predict_proba(X_test)[:, 1]
    threshold = DEFAULT_THRESHOLD
    y_pred = (y_prob >= threshold).astype(int)

    metrics = {
        "rows": int(len(cleaned)),
        "malicious_ratio": float(y.mean()),
        "threshold": float(threshold),
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred)),
        "recall": float(recall_score(y_test, y_pred)),
        "f1": float(f1_score(y_test, y_pred)),
        "roc_auc": float(roc_auc_score(y_test, y_prob)),
        "pr_auc": float(average_precision_score(y_test, y_prob)),
    }

    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, display_labels=["Safe", "Malicious"], cmap="Blues")
    plt.tight_layout()
    plt.savefig(processed_dir / "confusion_matrix.png", dpi=150)
    plt.close()

    RocCurveDisplay.from_predictions(y_test, y_prob)
    plt.tight_layout()
    plt.savefig(processed_dir / "roc_curve.png", dpi=150)
    plt.close()

    PrecisionRecallDisplay.from_predictions(y_test, y_prob)
    plt.tight_layout()
    plt.savefig(processed_dir / "precision_recall_curve.png", dpi=150)
    plt.close()

    payload = {
        "model": model,
        "feature_cols": FEATURE_SCHEMA,
        "threshold": threshold,
        "metrics": metrics,
    }
    joblib.dump(payload, model_dir / "best_model.joblib", compress=3)
    joblib.dump(scaler, model_dir / "scaler.joblib")
    (model_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-dir", default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args()
    metrics = train_project(args.base_dir)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

