import html
import json
import os
import sys
from datetime import datetime

import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from url_guard.inference import load_artifacts, predict_url


st.set_page_config(page_title="Malicious URL Guard", page_icon="🛡️", layout="wide")

st.markdown(
    """
<style>
:root {
    --panel: rgba(8, 18, 32, .78);
    --panel-strong: rgba(10, 24, 43, .94);
    --line: rgba(148, 163, 184, .22);
    --muted: #9fb0c7;
    --text: #f8fafc;
    --cyan: #2dd4bf;
    --rose: #fb7185;
    --amber: #fbbf24;
}
.stApp {
    background:
        radial-gradient(circle at 14% 10%, rgba(45, 212, 191, .16), transparent 28rem),
        radial-gradient(circle at 84% 18%, rgba(56, 189, 248, .12), transparent 28rem),
        linear-gradient(135deg, #07111f 0%, #0d1b2f 54%, #111827 100%);
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 1080px; padding-top: 2rem; padding-bottom: 2.2rem; }

.hero {
    border: 1px solid var(--line);
    border-radius: 8px;
    background: rgba(8, 18, 32, .70);
    padding: 1.25rem 1.35rem;
    margin-bottom: 1rem;
    box-shadow: 0 18px 70px rgba(0, 0, 0, .24);
}
.title {
    font-size: clamp(2rem, 4vw, 3.45rem);
    line-height: 1;
    font-weight: 880;
    margin-bottom: .55rem;
}
.subtitle {
    color: #b6c2d6;
    max-width: 760px;
    line-height: 1.55;
}
.layout {
    display: grid;
    grid-template-columns: minmax(0, 1.38fr) minmax(260px, .62fr);
    gap: 1rem;
}
.panel {
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--panel);
    padding: 1rem;
    box-shadow: 0 14px 48px rgba(0, 0, 0, .18);
}
.panel-title {
    font-weight: 820;
    color: #eef8ff;
    margin-bottom: .75rem;
}
.panel-title.centered { text-align: center; }
.panel-note {
    color: #cbd5e1;
    text-align: center;
    line-height: 1.45;
    margin: .1rem 0 1rem;
}
.example-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: .75rem;
    margin: .35rem 0 1rem;
}
.stButton > button {
    border-radius: 8px;
    min-height: 2.55rem;
    font-weight: 740;
    border: 1px solid rgba(148, 163, 184, .22);
    justify-content: center;
    text-align: center;
}
.stTextInput input {
    background: rgba(2, 6, 23, .68);
    border: 1px solid rgba(148, 163, 184, .30);
    color: #f8fafc;
    border-radius: 8px;
}
.result-card {
    border: 1px solid rgba(148, 163, 184, .22);
    border-radius: 8px;
    background: var(--panel-strong);
    padding: 1rem;
    margin-top: 1rem;
}
.risk-head {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
}
.risk-title {
    font-size: 1.25rem;
    font-weight: 820;
}
.risk-url {
    color: #cbd5e1;
    font-size: .88rem;
    margin-top: .35rem;
    overflow-wrap: anywhere;
}
.risk-score {
    font-size: 2rem;
    line-height: 1;
    font-weight: 900;
    white-space: nowrap;
}
.risk-track {
    height: 12px;
    background: #182235;
    border-radius: 999px;
    overflow: hidden;
    border: 1px solid rgba(148, 163, 184, .16);
    margin: .85rem 0 .2rem;
}
.risk-fill { height: 100%; border-radius: 999px; }
.quick-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: .55rem;
    margin-top: .8rem;
}
.quick-card {
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 8px;
    padding: .68rem;
    background: rgba(2, 6, 23, .36);
}
.quick-label { color: #94a3b8; font-size: .72rem; }
.quick-value { color: #f8fafc; font-size: .98rem; font-weight: 760; margin-top: .2rem; overflow-wrap: anywhere; }
.section-title {
    color: #f8fafc;
    font-weight: 800;
    margin: 1rem 0 .55rem;
}
.note {
    color: #d8e3f2;
    font-size: .9rem;
    padding: .42rem .55rem;
    border-left: 2px solid var(--cyan);
    background: rgba(45, 212, 191, .07);
    margin-bottom: .35rem;
}
.history-list { display: grid; gap: .55rem; }
.history-item {
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 8px;
    background: rgba(2, 6, 23, .36);
    padding: .62rem .68rem;
}
.history-url { color: #e2e8f0; font-size: .86rem; overflow-wrap: anywhere; }
.history-meta { color: #94a3b8; font-size: .76rem; margin-top: .18rem; }
.empty-state {
    color: #94a3b8;
    font-size: .9rem;
    border: 1px dashed rgba(148, 163, 184, .26);
    border-radius: 8px;
    padding: .85rem;
}
.feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(176px, 1fr));
    gap: .55rem;
}
.feature-chip {
    border: 1px solid rgba(148, 163, 184, .18);
    border-radius: 8px;
    padding: .58rem .65rem;
    background: rgba(2, 6, 23, .34);
    min-height: 68px;
}
.feature-name { color: #94a3b8; font-size: .72rem; overflow-wrap: anywhere; }
.feature-val { color: #f8fafc; font-size: .9rem; font-weight: 720; overflow-wrap: anywhere; margin-top: .25rem; }
.bottom-info {
    margin-top: 1.15rem;
    border: 1px solid rgba(148, 163, 184, .16);
    border-radius: 8px;
    background: rgba(2, 6, 23, .32);
    padding: .72rem .82rem;
    color: #9fb0c7;
    font-size: .82rem;
    display: flex;
    flex-wrap: wrap;
    gap: .65rem 1rem;
    justify-content: space-between;
}
.bottom-info strong { color: #cbd5e1; font-weight: 720; }

@media (max-width: 820px) {
    .layout { grid-template-columns: 1fr; }
    .example-grid, .quick-grid { grid-template-columns: 1fr 1fr; }
    .risk-head { flex-direction: column; }
}
@media (max-width: 560px) {
    .block-container { padding-left: .8rem; padding-right: .8rem; }
    .example-grid, .quick-grid { grid-template-columns: 1fr; }
    .hero, .panel, .result-card { padding: .85rem; }
}
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def cached_artifacts():
    return load_artifacts(BASE_DIR)


@st.cache_data(show_spinner=False)
def cached_metrics():
    metrics_path = os.path.join(BASE_DIR, "models", "metrics.json")
    if not os.path.exists(metrics_path):
        return {}
    with open(metrics_path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def add_history(prediction):
    item = {
        "time": datetime.now().strftime("%d.%m.%Y %H:%M"),
        "url": prediction.raw_url,
        "canonical": prediction.canonical_url,
        "risk": prediction.probability_malicious,
        "label": prediction.label,
    }
    if st.session_state.history and st.session_state.history[0].get("canonical") == item["canonical"]:
        return
    st.session_state.history = ([item] + st.session_state.history)[:8]


def risk_band(probability):
    if probability >= 0.75:
        return "Yüksek risk", "#fb7185"
    if probability >= 0.55:
        return "Dikkat gerekli", "#fbbf24"
    return "Düşük risk", "#2dd4bf"


def fmt_pct(value):
    return f"%{value * 100:.2f}"


FEATURE_LABELS = {
    "url_length": "URL uzunluğu",
    "hostname_length": "Alan adı uzunluğu",
    "path_length": "Yol uzunluğu",
    "path_length_no_slash": "Slash temizlenmiş yol uzunluğu",
    "query_length": "Sorgu uzunluğu",
    "num_dots": "Nokta sayısı",
    "num_hyphens": "Tire sayısı",
    "num_underscores": "Alt çizgi sayısı",
    "num_slashes": "Slash sayısı",
    "num_digits": "URL içindeki rakam sayısı",
    "num_params": "Parametre sayısı",
    "num_fragments": "Fragment işareti sayısı",
    "num_at_symbols": "@ işareti sayısı",
    "num_equals": "Eşittir işareti sayısı",
    "num_ampersands": "Ampersand işareti sayısı",
    "num_percent": "Yüzde işareti sayısı",
    "num_subdomains": "Alt alan adı sayısı",
    "subdomain_depth": "Alt alan derinliği",
    "has_ip": "IP adresi kullanıyor mu",
    "has_at_symbol": "@ işareti içeriyor mu",
    "has_double_slash": "Fazladan çift slash var mı",
    "has_www": "WWW ile başlıyor mu",
    "has_port": "Özel port kullanıyor mu",
    "port_number": "Port numarası",
    "has_hex_encoding": "Kodlanmış karakter içeriyor mu",
    "has_punycode": "Punycode içeriyor mu",
    "is_shortened": "URL kısaltıcı mı",
    "has_suspicious_tld": "Şüpheli uzantı mı",
    "has_trusted_tld": "Güvenilir uzantı mı",
    "is_net_tld": ".net uzantısı mı",
    "is_edu_tld": ".edu uzantısı mı",
    "has_abused_country_tld": "Riskli ülke uzantısı mı",
    "tld_length": "Uzantı uzunluğu",
    "url_entropy": "URL karmaşıklık skoru",
    "domain_entropy": "Alan adı karmaşıklık skoru",
    "domain_core_entropy": "Ana domain karmaşıklık skoru",
    "domain_core_length": "Ana domain uzunluğu",
    "digit_ratio": "Rakam oranı",
    "letter_ratio": "Harf oranı",
    "special_char_ratio": "Özel karakter oranı",
    "vowel_ratio": "Sesli harf oranı",
    "num_tokens": "Parça sayısı",
    "avg_token_length": "Ortalama parça uzunluğu",
    "max_token_length": "En uzun parça uzunluğu",
    "max_consecutive_digits": "En uzun ardışık rakam",
    "num_suspicious_keywords": "Şüpheli kelime sayısı",
    "has_suspicious_keywords": "Şüpheli kelime içeriyor mu",
    "brand_in_url": "Marka adı URL içinde mi",
    "brand_in_subdomain": "Marka adı alt alanda mı",
    "brand_in_path": "Marka adı yolda mı",
    "url_depth": "URL yol derinliği",
    "effective_url_depth": "Temizlenmiş yol derinliği",
    "trailing_slash": "Sonda slash var mı",
    "is_root_path": "Ana sayfa yolu mu",
    "domain_has_digits": "Domain rakam içeriyor mu",
    "has_exec_extension": "Çalıştırılabilir dosya uzantısı mı",
    "has_script_extension": "Script dosyası uzantısı mı",
    "is_valid_url": "Geçerli URL mi",
}

BINARY_FEATURES = {
    "has_ip",
    "has_at_symbol",
    "has_double_slash",
    "has_www",
    "has_port",
    "has_hex_encoding",
    "has_punycode",
    "is_shortened",
    "has_suspicious_tld",
    "has_trusted_tld",
    "is_net_tld",
    "is_edu_tld",
    "has_abused_country_tld",
    "has_suspicious_keywords",
    "brand_in_url",
    "brand_in_subdomain",
    "brand_in_path",
    "trailing_slash",
    "is_root_path",
    "domain_has_digits",
    "has_exec_extension",
    "has_script_extension",
    "is_valid_url",
}


def feature_label(key):
    return FEATURE_LABELS.get(key, key.replace("_", " ").capitalize())


def feature_value(key, val):
    if key in BINARY_FEATURES:
        return "Evet" if int(val) == 1 else "Hayır"
    if isinstance(val, float):
        return f"{val:.6f}" if abs(val) < 1 else f"{val:.4f}"
    return str(val)


try:
    payload, scaler = cached_artifacts()
except FileNotFoundError:
    st.error("Model dosyaları bulunamadı. Önce `python -m url_guard.train --base-dir .` komutunu çalıştırın.")
    st.stop()

metrics = cached_metrics()

if "url_input" not in st.session_state:
    st.session_state.url_input = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None

st.markdown(
    """
<div class="hero">
  <div class="title">Malicious URL Guard</div>
  <div class="subtitle">Bağlantıyı açmadan önce riskini hızlıca kontrol edin.</div>
</div>
""",
    unsafe_allow_html=True,
)

examples = {
    "Güvenli örnek": "https://google.com",
    "Marka taklidi": "https://paypal.security-check.example.com/login",
    "Kısaltıcı": "https://bit.ly/abc123",
    "Dosya riski": "https://example.com/download/invoice.exe",
}

main_col, side_col = st.columns([1.4, .6], gap="large")

with main_col:
    st.markdown(
        '<div class="panel"><div class="panel-note">Aşağıdaki butonlara tıklayarak örnek URL denemeleri yapabilirsiniz.</div>',
        unsafe_allow_html=True,
    )
    example_cols = st.columns(len(examples), gap="medium")
    for col, (label, value) in zip(example_cols, examples.items()):
        if col.button(label, use_container_width=True):
            st.session_state.url_input = value

    st.markdown('<div class="section-title">URL Sorgulama</div>', unsafe_allow_html=True)
    with st.form("analysis_form"):
        url_input = st.text_input("URL", key="url_input", placeholder="https://example.com/login?token=123")
        analyze = st.form_submit_button("Analiz et", type="primary", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze:
        if not url_input.strip():
            st.warning("Bir URL girmen gerekiyor.")
        else:
            prediction = predict_url(url_input, payload, scaler)
            st.session_state.last_prediction = prediction
            add_history(prediction)

    prediction = st.session_state.last_prediction
    if prediction:
        risk_pct = prediction.probability_malicious * 100
        band, risk_color = risk_band(prediction.probability_malicious)
        status_text = "Riskli / kötücül olabilir" if prediction.label else "Muhtemelen güvenli"
        quick_items = [
            ("Risk bandı", band),
            ("Güvenli olasılığı", fmt_pct(prediction.probability_safe)),
            ("Eşik", fmt_pct(prediction.threshold)),
        ]

        st.markdown(
            f"""
<div class="result-card">
  <div class="risk-head">
    <div>
      <div class="risk-title">{html.escape(status_text)}</div>
      <div class="risk-url">{html.escape(prediction.canonical_url)}</div>
    </div>
    <div class="risk-score" style="color: {risk_color};">%{risk_pct:.2f}</div>
  </div>
  <div class="risk-track"><div class="risk-fill" style="width: {risk_pct:.2f}%; background: {risk_color};"></div></div>
  <div class="quick-grid">
    {''.join(f'<div class="quick-card"><div class="quick-label">{html.escape(k)}</div><div class="quick-value">{html.escape(v)}</div></div>' for k, v in quick_items)}
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        tab_summary, tab_anatomy, tab_features = st.tabs(["Özeti", "Anatomisi", "Tüm Özellikleri"])
        with tab_summary:
            if prediction.notes:
                for note in prediction.notes:
                    st.markdown(f'<div class="note">{html.escape(note)}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state">Ek kural notu yok; sonuç model skorundan geliyor.</div>', unsafe_allow_html=True)

        with tab_anatomy:
            anatomy = [
                ("Host uzunluğu", prediction.features.get("hostname_length", 0)),
                ("Path uzunluğu", prediction.features.get("path_length", 0)),
                ("Query uzunluğu", prediction.features.get("query_length", 0)),
                ("Alt alan derinliği", prediction.features.get("subdomain_depth", 0)),
                ("Şüpheli kelime", prediction.features.get("num_suspicious_keywords", 0)),
                ("URL uzunluğu", prediction.features.get("url_length", 0)),
                ("IP kullanımı", "Evet" if prediction.features.get("has_ip", 0) else "Hayır"),
                ("Kısaltıcı", "Evet" if prediction.features.get("is_shortened", 0) else "Hayır"),
            ]
            st.markdown(
                '<div class="feature-grid">'
                + "".join(
                    f'<div class="feature-chip"><div class="feature-name">{html.escape(str(k))}</div><div class="feature-val">{html.escape(str(v))}</div></div>'
                    for k, v in anatomy
                )
                + "</div>",
                unsafe_allow_html=True,
            )

        with tab_features:
            chips = ['<div class="feature-grid">']
            for key in payload["feature_cols"]:
                val = prediction.features.get(key, 0)
                val_text = feature_value(key, val)
                chips.append(
                    f'<div class="feature-chip"><div class="feature-name">{html.escape(feature_label(key))}</div>'
                    f'<div class="feature-val">{html.escape(val_text)}</div></div>'
                )
            chips.append("</div>")
            st.markdown("".join(chips), unsafe_allow_html=True)

with side_col:
    st.markdown('<div class="panel"><div class="panel-title centered">Geçmiş</div>', unsafe_allow_html=True)
    if st.session_state.history:
        st.markdown('<div class="history-list">', unsafe_allow_html=True)
        for item in st.session_state.history:
            status = "Riskli" if item["label"] else "Güvenli"
            color = "#fb7185" if item["label"] else "#2dd4bf"
            st.markdown(
                f"""
<div class="history-item">
  <div class="history-url">{html.escape(item["url"])}</div>
  <div class="history-meta"><span style="color:{color};">{status}</span> · {fmt_pct(item["risk"])} · {html.escape(item["time"])}</div>
</div>
""",
                unsafe_allow_html=True,
            )
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown('<div class="empty-state">Henüz sorgu yok.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f"""
<div class="bottom-info">
  <span><strong>Test ROC-AUC:</strong> {metrics.get("roc_auc", 0):.3f}</span>
  <span><strong>Precision:</strong> {metrics.get("precision", 0):.3f}</span>
  <span><strong>Recall:</strong> {metrics.get("recall", 0):.3f}</span>
  <span><strong>Temiz veri:</strong> {int(metrics.get("rows", 0)):,} satır</span>
  <span>Karar destek amaçlıdır; kritik güvenlik kararlarında tek kaynak olarak kullanılmamalıdır.</span>
</div>
""",
    unsafe_allow_html=True,
)
