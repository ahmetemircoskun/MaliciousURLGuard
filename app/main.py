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
.example-grid {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: .75rem;
    margin-top: .85rem;
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
    cursor: help;
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
    "url_length": "URL Uzunluğu",
    "hostname_length": "Alan Adı Uzunluğu",
    "path_length": "Yol Uzunluğu",
    "path_length_no_slash": "Slash Temizlenmiş Yol Uzunluğu",
    "query_length": "Sorgu Uzunluğu",
    "num_dots": "Nokta Sayısı",
    "num_hyphens": "Tire Sayısı",
    "num_underscores": "Alt Çizgi Sayısı",
    "num_slashes": "Slash Sayısı",
    "num_digits": "URL İçindeki Rakam Sayısı",
    "num_params": "Parametre Sayısı",
    "num_fragments": "Fragment İşareti Sayısı",
    "num_at_symbols": "@ İşareti Sayısı",
    "num_equals": "Eşittir İşareti Sayısı",
    "num_ampersands": "Ampersand İşareti Sayısı",
    "num_percent": "Yüzde İşareti Sayısı",
    "num_subdomains": "Alt Alan Adı Sayısı",
    "subdomain_depth": "Alt Alan Derinliği",
    "has_ip": "IP Adresi Kullanıyor Mu",
    "has_at_symbol": "@ İşareti İçeriyor Mu",
    "has_double_slash": "Fazladan Çift Slash Var Mı",
    "has_www": "WWW İle Başlıyor Mu",
    "has_port": "Özel Port Kullanıyor Mu",
    "port_number": "Port Numarası",
    "has_hex_encoding": "Kodlanmış Karakter İçeriyor Mu",
    "has_punycode": "Punycode İçeriyor Mu",
    "is_shortened": "URL Kısaltıcı Mı",
    "has_suspicious_tld": "Şüpheli Uzantı Mı",
    "has_trusted_tld": "Güvenilir Uzantı Mı",
    "is_net_tld": ".net Uzantısı Mı",
    "is_edu_tld": "Eğitim Alanı Uzantısı Mı",
    "has_abused_country_tld": "Riskli Ülke Uzantısı Mı",
    "tld_length": "Uzantı Uzunluğu",
    "url_entropy": "URL Karmaşıklık Skoru",
    "domain_entropy": "Alan Adı Karmaşıklık Skoru",
    "domain_core_entropy": "Ana Domain Karmaşıklık Skoru",
    "domain_core_length": "Ana Domain Uzunluğu",
    "digit_ratio": "Rakam Oranı",
    "letter_ratio": "Harf Oranı",
    "special_char_ratio": "Özel Karakter Oranı",
    "vowel_ratio": "Sesli Harf Oranı",
    "num_tokens": "Parça Sayısı",
    "avg_token_length": "Ortalama Parça Uzunluğu",
    "max_token_length": "En Uzun Parça Uzunluğu",
    "max_consecutive_digits": "En Uzun Ardışık Rakam",
    "num_suspicious_keywords": "Şüpheli Kelime Sayısı",
    "has_suspicious_keywords": "Şüpheli Kelime İçeriyor Mu",
    "brand_in_url": "Marka Adı URL İçinde Mi",
    "brand_in_subdomain": "Marka Adı Alt Alanda Mı",
    "brand_in_path": "Marka Adı Yolda Mı",
    "url_depth": "URL Yol Derinliği",
    "effective_url_depth": "Temizlenmiş Yol Derinliği",
    "trailing_slash": "Sonda Slash Var Mı",
    "is_root_path": "Ana Sayfa Yolu Mu",
    "domain_has_digits": "Domain Rakam İçeriyor Mu",
    "has_exec_extension": "Çalıştırılabilir Dosya Uzantısı Mı",
    "has_script_extension": "Script Dosyası Uzantısı Mı",
    "is_valid_url": "Geçerli URL Mi",
}

FEATURE_HINTS = {
    "url_length": "Kanonik hale getirilmiş URL'nin toplam karakter sayısıdır.",
    "hostname_length": "Alan adı bölümünün, yani host kısmının uzunluğunu gösterir.",
    "path_length": "Alan adından sonra gelen yol bölümünün karakter uzunluğudur.",
    "query_length": "Soru işaretinden sonra gelen parametre bölümünün uzunluğudur.",
    "num_dots": "URL içindeki nokta karakterlerinin toplam sayısıdır.",
    "num_hyphens": "URL içinde kaç tire kullanıldığını gösterir.",
    "num_digits": "URL metnindeki toplam rakam sayısıdır.",
    "num_params": "Query içinde tahmini kaç parametre olduğunu gösterir.",
    "num_subdomains": "Ana domainin solundaki alt alan adı sayısıdır.",
    "subdomain_depth": "Alt alan adlarının ne kadar derin olduğunu gösterir.",
    "has_ip": "Alan adı yerine doğrudan IP adresi kullanılıp kullanılmadığını gösterir.",
    "has_at_symbol": "@ işareti bazı URL'lerde gerçek hostu gizlemek için kullanılabilir.",
    "has_double_slash": "Şema dışındaki fazladan çift slash kullanımını gösterir.",
    "has_www": "Alan adının www ile başlayıp başlamadığını gösterir.",
    "has_port": "URL'nin varsayılan dışında port kullanıp kullanmadığını gösterir.",
    "port_number": "Varsa URL'de kullanılan port numarasıdır.",
    "has_hex_encoding": "URL'de yüzde kodlamasıyla gizlenmiş karakter olup olmadığını gösterir.",
    "has_punycode": "Uluslararası alan adlarında kullanılan punycode biçimini gösterir.",
    "is_shortened": "URL'nin kısaltıcı servis üzerinden gelip gelmediğini gösterir.",
    "has_suspicious_tld": "Alan adı uzantısının sık kötüye kullanılan listede olup olmadığını gösterir.",
    "has_trusted_tld": "Alan adı uzantısının yaygın ve güvenilir kabul edilen grupta olup olmadığını gösterir.",
    "is_edu_tld": "Alan adının eğitim kurumu uzantısı taşıyıp taşımadığını gösterir.",
    "url_entropy": "URL'nin rastgele veya karmaşık görünüp görünmediğini ölçen değerdir.",
    "domain_entropy": "Alan adı bölümünün karakter karmaşıklığını gösterir.",
    "domain_core_entropy": "Ana domain etiketinin karakter karmaşıklığını gösterir.",
    "digit_ratio": "URL içindeki rakamların tüm karakterlere oranıdır.",
    "letter_ratio": "URL içindeki harflerin tüm karakterlere oranıdır.",
    "special_char_ratio": "Harf ve rakam dışındaki karakterlerin oranıdır.",
    "num_suspicious_keywords": "URL içinde yakalanan şüpheli kelime sayısıdır.",
    "has_suspicious_keywords": "URL'nin login, verify, account gibi şüpheli kelimeler içerip içermediğini gösterir.",
    "brand_in_url": "Marka adının URL içinde geçip geçmediğini gösterir.",
    "brand_in_subdomain": "Marka adının alt alan adı kısmında geçip geçmediğini gösterir.",
    "brand_in_path": "Marka adının yol kısmında geçip geçmediğini gösterir.",
    "url_depth": "Yol bölümünün kaç parçadan oluştuğunu gösterir.",
    "is_root_path": "URL'nin doğrudan ana sayfaya gidip gitmediğini gösterir.",
    "domain_has_digits": "Ana domain adında rakam bulunup bulunmadığını gösterir.",
    "has_exec_extension": "URL'nin exe, zip, msi gibi riskli dosya uzantısıyla bitip bitmediğini gösterir.",
    "has_script_extension": "URL'nin php, asp gibi script uzantısıyla bitip bitmediğini gösterir.",
    "is_valid_url": "URL'nin teknik olarak geçerli ayrıştırılıp ayrıştırılamadığını gösterir.",
}

DEFAULT_FEATURE_HINT = "Bu değer URL'nin yapısından çıkarılan model girdilerinden biridir."

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


def feature_hint(key):
    return FEATURE_HINTS.get(key, DEFAULT_FEATURE_HINT)


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
    "Güvenli Örnek": "https://google.com",
    "Marka Taklidi": "https://paypal.security-check.example.com/login",
    "Kısaltıcı": "https://bit.ly/abc123",
    "Dosya Riski": "https://example.com/download/invoice.exe",
}

main_col, side_col = st.columns([1.4, .6], gap="large")

with main_col:
    st.markdown('<div class="panel"><div class="section-title">URL Sorgulama</div>', unsafe_allow_html=True)
    with st.form("analysis_form"):
        url_input = st.text_input("URL", key="url_input", placeholder="https://example.com/login?token=123")
        analyze = st.form_submit_button("Analiz Et", type="primary", use_container_width=True)
    example_cols = st.columns(len(examples), gap="medium")
    for col, (label, value) in zip(example_cols, examples.items()):
        if col.button(label, use_container_width=True):
            st.session_state.url_input = value
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
            ("Risk Bandı", band),
            ("Güvenli Olasılığı", fmt_pct(prediction.probability_safe)),
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
                ("Host Uzunluğu", prediction.features.get("hostname_length", 0), "Alan adı bölümünün toplam karakter uzunluğudur."),
                ("Path Uzunluğu", prediction.features.get("path_length", 0), "Alan adından sonra gelen yol bölümünün uzunluğudur."),
                ("Query Uzunluğu", prediction.features.get("query_length", 0), "Parametre bölümünün karakter uzunluğudur."),
                ("Alt Alan Derinliği", prediction.features.get("subdomain_depth", 0), "Ana domainden önce kaç alt alan katmanı olduğunu gösterir."),
                ("Şüpheli Kelime", prediction.features.get("num_suspicious_keywords", 0), "URL içinde yakalanan şüpheli kelime sayısıdır."),
                ("URL Uzunluğu", prediction.features.get("url_length", 0), "Kanonik URL'nin toplam karakter sayısıdır."),
                ("IP Kullanımı", "Evet" if prediction.features.get("has_ip", 0) else "Hayır", "Alan adı yerine IP adresi kullanılıp kullanılmadığını gösterir."),
                ("Kısaltıcı", "Evet" if prediction.features.get("is_shortened", 0) else "Hayır", "URL'nin kısaltıcı servis üzerinden gelip gelmediğini gösterir."),
            ]
            st.markdown(
                '<div class="feature-grid">'
                + "".join(
                    f'<div class="feature-chip" title="{html.escape(str(h), quote=True)}"><div class="feature-name">{html.escape(str(k))}</div><div class="feature-val">{html.escape(str(v))}</div></div>'
                    for k, v, h in anatomy
                )
                + "</div>",
                unsafe_allow_html=True,
            )

        with tab_features:
            chips = ['<div class="feature-grid">']
            for key in payload["feature_cols"]:
                val = prediction.features.get(key, 0)
                val_text = feature_value(key, val)
                hint = feature_hint(key)
                chips.append(
                    f'<div class="feature-chip" title="{html.escape(hint, quote=True)}"><div class="feature-name">{html.escape(feature_label(key))}</div>'
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
  <span><strong>Temizlenmiş Veri:</strong> {int(metrics.get("rows", 0)):,} satır</span>
  <span>Karar destek amaçlıdır; kritik güvenlik kararlarında tek kaynak olarak kullanılmamalıdır.</span>
</div>
""",
    unsafe_allow_html=True,
)
