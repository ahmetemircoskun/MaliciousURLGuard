"""Dataset loading and cleaning."""

from __future__ import annotations

import re

import pandas as pd

from .url_tools import canonicalize_url

SECRET_SHAPED_PATTERNS = [
    re.compile(r"(?:AKIA|ASIA)[0-9A-Z]{16}"),
    re.compile(r"(?:AWSAccessKeyId|X-Amz-Credential|X-Amz-Signature|Signature)=", re.I),
    re.compile(r"(?<![A-Za-z0-9/+])[A-Za-z0-9/+]{40,}={0,2}(?![A-Za-z0-9/+])"),
]


def has_secret_shaped_token(url: str) -> bool:
    text = str(url)
    return any(pattern.search(text) for pattern in SECRET_SHAPED_PATTERNS)


def clean_dataset(raw_path: str) -> pd.DataFrame:
    raw = pd.read_csv(raw_path)
    required = {"url", "type"}
    missing = required - set(raw.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    work = raw.dropna(subset=["url", "type"]).copy()
    work["type"] = work["type"].astype(str).str.strip().str.lower()
    work = work[~work["url"].astype(str).apply(has_secret_shaped_token)].copy()

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
