from url_guard.features import extract_features
from url_guard.inference import load_artifacts, predict_url
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


def test_edu_tr_domain_is_parsed_as_registrable_domain():
    parts = canonicalize_url("https://gazi.edu.tr")
    features = extract_features("https://gazi.edu.tr")
    assert parts.registrable_domain == "gazi.edu.tr"
    assert parts.domain_core == "gazi"
    assert parts.tld == ".edu.tr"
    assert features["is_edu_tld"] == 1
    assert features["has_trusted_tld"] == 1


def test_gazi_edu_tr_prediction_is_safe():
    payload, scaler = load_artifacts(".")
    prediction = predict_url("https://gazi.edu.tr", payload, scaler)
    assert prediction.label == 0
