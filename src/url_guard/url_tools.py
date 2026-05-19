"""URL parsing and normalization utilities."""

from __future__ import annotations

import ipaddress
import re
import string
from dataclasses import dataclass
from urllib.parse import unquote, urlparse, urlunparse

CONTROL_CHARS = set(chr(i) for i in range(32)) | {chr(127)}
DOMAIN_LABEL_RE = re.compile(r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$")


@dataclass(frozen=True)
class UrlParts:
    raw: str
    canonical: str
    scheme: str
    host: str
    path: str
    query: str
    port: int | None
    tld: str
    registrable_domain: str
    domain_core: str
    subdomain: str
    is_valid: bool
    reason: str = ""


def ensure_scheme(url: str) -> str:
    text = str(url).strip()
    if not text.lower().startswith(("http://", "https://", "ftp://")):
        text = "https://" + text
    return text


def _has_bad_chars(text: str) -> bool:
    if any(ch in CONTROL_CHARS for ch in text):
        return True
    return any(ch not in string.printable for ch in text)


def _idna_host(host: str) -> str | None:
    host = host.strip().strip(".").lower()
    if not host:
        return None
    try:
        return host.encode("idna").decode("ascii")
    except UnicodeError:
        return None


def _is_ipv4(host: str) -> bool:
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


def _valid_host(host: str) -> bool:
    if _is_ipv4(host):
        return True
    labels = host.split(".")
    if len(labels) < 2:
        return False
    return all(DOMAIN_LABEL_RE.match(label) for label in labels)


def split_host(host: str) -> tuple[str, str, str, str]:
    """Return tld, registrable domain, core label, subdomain.

    The Kaggle dataset mostly contains common one-label public suffixes.
    A small multi-part suffix list prevents obvious mistakes for co.uk/com.br.
    """
    if _is_ipv4(host):
        return "", host, host, ""
    labels = host.split(".")
    multi_suffixes = {
        ("co", "uk"), ("com", "br"), ("com", "au"), ("co", "jp"),
        ("co", "in"), ("com", "tr"), ("com", "cn"), ("co", "za"),
    }
    if len(labels) >= 3 and tuple(labels[-2:]) in multi_suffixes:
        tld_labels = labels[-2:]
        core_index = -3
    else:
        tld_labels = labels[-1:]
        core_index = -2
    tld = "." + ".".join(tld_labels)
    core = labels[core_index]
    registrable = ".".join([core, *tld_labels])
    subdomain = ".".join(labels[:core_index]) if len(labels[:core_index]) else ""
    return tld, registrable, core, subdomain


def canonicalize_url(url: str) -> UrlParts:
    raw = str(url).strip()
    if not raw or _has_bad_chars(raw):
        return UrlParts(raw, raw, "", "", "", "", None, "", "", "", "", False, "invalid characters")

    prepared = ensure_scheme(raw)
    try:
        parsed = urlparse(prepared)
    except Exception:
        return UrlParts(raw, prepared, "", "", "", "", None, "", "", "", "", False, "parse failed")

    scheme = (parsed.scheme or "https").lower()
    host = _idna_host(parsed.hostname or "")
    if host is None or not _valid_host(host):
        return UrlParts(raw, prepared, scheme, host or "", "", "", None, "", "", "", "", False, "invalid host")

    try:
        port = parsed.port
    except ValueError:
        port = None

    path = unquote(parsed.path or "", errors="ignore")
    if _has_bad_chars(path):
        return UrlParts(raw, prepared, scheme, host, path, "", port, "", "", "", "", False, "invalid path")
    if path == "/":
        path = ""
    elif path.endswith("/") and len(path) > 1:
        path = path.rstrip("/")

    query = parsed.query or ""
    if _has_bad_chars(query):
        return UrlParts(raw, prepared, scheme, host, path, query, port, "", "", "", "", False, "invalid query")

    if scheme == "ftp":
        netloc = f"{host}:{port}" if port is not None else host
        canonical = urlunparse(("ftp", netloc, path, "", query, ""))
    else:
        scheme = "https"
        netloc = host if port in (None, 80, 443) else f"{host}:{port}"
        canonical = urlunparse((scheme, netloc, path, "", query, ""))

    tld, registrable, core, subdomain = split_host(host)
    return UrlParts(raw, canonical, scheme, host, path, query, port, tld, registrable, core, subdomain, True)

