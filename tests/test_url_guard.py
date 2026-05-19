from url_guard.features import extract_features
from url_guard.url_tools import canonicalize_url


def test_canonicalize_collapses_default_http_https():
    a = canonicalize_url("http://Example.com:80/login/")
    b = canonicalize_url("https://example.com/login")
    assert a.is_valid
    assert a.canonical == b.canonical == "https://example.com/login"


def test_rejects_control_character_urls():
    parts = canonicalize_url("https://\x05bad.example.com")
    assert not parts.is_valid


def test_brand_impersonation_features():
    features = extract_features("https://paypal.security-check.example.com/login")
    assert features["brand_in_subdomain"] == 1
    assert features["brand_in_url"] == 1

