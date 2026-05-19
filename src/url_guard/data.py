"""Dataset loading and cleaning."""

from __future__ import annotations

import pandas as pd

from .url_tools import canonicalize_url


def clean_dataset(raw_path: str) -> pd.DataFrame:
    raw = pd.read_csv(raw_path)
    required = {"url", "type"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    work = raw.dropna(subset=["url", "type"]).copy()
    work["type"] = work["type"].astype(str).str.strip().str.lower()

    records = []
    for row in work.itertuples(index=False):
        parts = canonicalize_url(row.url)
        if not parts.is_valid:
            continue
        label = 0 if row.type == "benign" else 1
        records.append((parts.canonical, label, row.type))

    cleaned = pd.DataFrame(records, columns=["url", "label", "source_type"])
    if cleaned.empty:
        raise ValueError("No valid URLs left after cleaning.")

    merged = (
        cleaned.sort_values(["url", "label"])
        .groupby("url", as_index=False)
        .agg(label=("label", "max"), source_type=("source_type", lambda values: ",".join(sorted(set(values)))))
    )
    return merged

