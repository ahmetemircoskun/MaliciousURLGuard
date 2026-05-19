"""Feature extraction shared by training and inference."""

from __future__ import annotations

import math
import os
import re

from .config import (
    ABUSED_COUNTRY_TLDS,
    BRANDS,
    EXECUTABLE_EXTENSIONS,
    SCRIPT_EXTENSIONS,
    SHORTENER_DOMAINS,
    SUSPICIOUS_KEYWORDS,
    SUSPICIOUS_TLDS,
    TRUSTED_TLDS,
)
from .url_tools import canonicalize_url


FEATURE_SCHEMA = [
    "url_length", "hostname_length", "path_length", "path_length_no_slash",
    "query_length", "num_dots", "num_hyphens", "num_underscores",
    "num_slashes", "num_digits", "num_params", "num_fragments",
    "num_at_symbols", "num_equals", "num_ampersands", "num_percent",
    "num_subdomains", "subdomain_depth", "has_ip", "has_at_symbol",
    "has_double_slash", "has_www", "has_port", "port_number",
    "has_hex_encoding", "has_punycode", "is_shortened",
    "has_suspicious_tld", "has_trusted_tld", "is_net_tld", "is_edu_tld",
    "has_abused_country_tld", "tld_length", "url_entropy",
    "domain_entropy", "domain_core_entropy", "domain_core_length",
    "digit_ratio", "letter_ratio", "special_char_ratio", "vowel_ratio",
    "num_tokens", "avg_token_length", "max_token_length",
    "max_consecutive_digits", "num_suspicious_keywords",
    "has_suspicious_keywords", "brand_in_url", "brand_in_subdomain",
    "brand_in_path", "url_depth", "effective_url_depth", "trailing_slash",
    "is_root_path", "domain_has_digits", "has_exec_extension",
    "has_script_extension", "is_valid_url",
]


def entropy(text: str) -> float:
    if not text:
        return 0.0
    counts: dict[str, int] = {}
    for char in text:
        counts[char] = counts.get(char, 0) + 1
    n = len(text)
    return -sum((count / n) * math.log2(count / n) for count in counts.values())


def _is_ip(host: str) -> bool:
    return bool(re.match(r"^(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)$", host))


def extract_features(url: str) -> dict[str, float]:
    parts = canonicalize_url(url)
    canonical = parts.canonical
    url_lower = canonical.lower()
    host = parts.host
    path = parts.path
    query = parts.query
    path_stripped = path.rstrip("/")

    f: dict[str, float] = {}
    f["url_length"] = len(canonical)
    f["hostname_length"] = len(host)
    f["path_length"] = len(path)
    f["path_length_no_slash"] = len(path_stripped)
    f["query_length"] = len(query)

    f["num_dots"] = canonical.count(".")
    f["num_hyphens"] = canonical.count("-")
    f["num_underscores"] = canonical.count("_")
    f["num_slashes"] = canonical.count("/")
    f["num_digits"] = sum(c.isdigit() for c in canonical)
    f["num_params"] = query.count("&") + (1 if query else 0)
    f["num_fragments"] = str(url).count("#")
    f["num_at_symbols"] = canonical.count("@")
    f["num_equals"] = canonical.count("=")
    f["num_ampersands"] = canonical.count("&")
    f["num_percent"] = canonical.count("%")

    subdomain_labels = [x for x in parts.subdomain.split(".") if x]
    f["num_subdomains"] = len(subdomain_labels)
    f["subdomain_depth"] = len(subdomain_labels)

    f["has_ip"] = int(_is_ip(host))
    f["has_at_symbol"] = int("@" in canonical)
    f["has_double_slash"] = int("//" in canonical.split("://", 1)[-1])
    f["has_www"] = int(host.startswith("www."))
    f["has_port"] = int(bool(parts.port and parts.port not in (80, 443)))
    f["port_number"] = parts.port if parts.port else 0
    f["has_hex_encoding"] = int(bool(re.search(r"%[0-9a-fA-F]{2}", str(url))))
    f["has_punycode"] = int("xn--" in host)
    f["is_shortened"] = int(host in SHORTENER_DOMAINS or parts.registrable_domain in SHORTENER_DOMAINS)

    f["has_suspicious_tld"] = int(parts.tld in SUSPICIOUS_TLDS)
    f["has_trusted_tld"] = int(parts.tld in TRUSTED_TLDS)
    f["is_net_tld"] = int(parts.tld == ".net")
    f["is_edu_tld"] = int(parts.tld == ".edu")
    f["has_abused_country_tld"] = int(parts.tld in ABUSED_COUNTRY_TLDS)
    f["tld_length"] = len(parts.tld)

    f["url_entropy"] = entropy(canonical)
    f["domain_entropy"] = entropy(host)
    f["domain_core_entropy"] = entropy(parts.domain_core)
    f["domain_core_length"] = len(parts.domain_core)

    url_len = max(len(canonical), 1)
    letters = [c for c in canonical if c.isalpha()]
    f["digit_ratio"] = sum(c.isdigit() for c in canonical) / url_len
    f["letter_ratio"] = len(letters) / url_len
    f["special_char_ratio"] = sum(not c.isalnum() for c in canonical) / url_len
    f["vowel_ratio"] = sum(c in "aeiouAEIOU" for c in letters) / max(len(letters), 1)

    tokens = [t for t in re.split(r"[.\-/_?&=#+@:%]", url_lower) if t]
    f["num_tokens"] = len(tokens)
    f["avg_token_length"] = sum(len(t) for t in tokens) / max(len(tokens), 1)
    f["max_token_length"] = max((len(t) for t in tokens), default=0)
    f["max_consecutive_digits"] = max((len(m) for m in re.findall(r"\d+", canonical)), default=0)

    keyword_hits = sum(keyword in url_lower for keyword in SUSPICIOUS_KEYWORDS)
    f["num_suspicious_keywords"] = keyword_hits
    f["has_suspicious_keywords"] = int(keyword_hits > 0)

    brand_is_primary = parts.domain_core in BRANDS
    f["brand_in_url"] = int(any(brand in url_lower for brand in BRANDS) and not brand_is_primary)
    f["brand_in_subdomain"] = int(any(brand in parts.subdomain for brand in BRANDS) and not brand_is_primary)
    f["brand_in_path"] = int(any(brand in path.lower() for brand in BRANDS) and not brand_is_primary)

    f["url_depth"] = len([segment for segment in path.split("/") if segment])
    f["effective_url_depth"] = len([segment for segment in path_stripped.split("/") if segment])
    f["trailing_slash"] = int(path.endswith("/") and len(path) > 1)
    f["is_root_path"] = int(path in ("", "/"))
    f["domain_has_digits"] = int(any(c.isdigit() for c in parts.domain_core))

    _, ext = os.path.splitext(path.lower())
    f["has_exec_extension"] = int(ext in EXECUTABLE_EXTENSIONS)
    f["has_script_extension"] = int(ext in SCRIPT_EXTENSIONS)
    f["is_valid_url"] = int(parts.is_valid)

    return {name: f.get(name, 0.0) for name in FEATURE_SCHEMA}

