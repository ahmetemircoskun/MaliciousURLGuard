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
div[data-testid="stRadio"] {
    border: 1px solid var(--line);
    border-radius: 8px;
    background: rgba(8, 18, 32, .62);
    padding: .35rem .6rem;
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
def cached_metrics(metrics_mtime):
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


def t(key, lang):
    return TEXT[lang][key]


def translate_note(note, lang):
    if lang == "EN":
        return NOTE_TRANSLATIONS.get(note, note)
    return note


def risk_band(probability, lang):
    if probability >= 0.75:
        return t("high_risk", lang), "#fb7185"
    if probability >= 0.55:
        return t("medium_risk", lang), "#fbbf24"
    return t("low_risk", lang), "#2dd4bf"


def fmt_pct(value):
    return f"%{value * 100:.2f}"


TEXT = {
    "TR": {
        "subtitle": "Bağlantıyı açmadan önce riskini hızlıca kontrol edin.",
        "analyze": "Analiz Et",
        "empty_url": "Bir URL girmen gerekiyor.",
        "model_missing": "Model dosyaları bulunamadı. Önce `python -m url_guard.train --base-dir .` komutunu çalıştırın.",
        "safe_example": "Güvenli Örnek",
        "brand_spoof": "Marka Taklidi",
        "shortener": "Kısaltıcı",
        "file_risk": "Dosya Riski",
        "risky_status": "Riskli / kötücül olabilir",
        "safe_status": "Muhtemelen güvenli",
        "risk_band": "Risk Bandı",
        "safe_probability": "Güvenli Olasılığı",
        "threshold": "Eşik",
        "summary": "Özeti",
        "anatomy": "Anatomisi",
        "all_features": "Tüm Özellikleri",
        "no_rule_note": "Ek kural notu yok; sonuç model skorundan geliyor.",
        "history": "Geçmiş",
        "no_history": "Henüz sorgu yok.",
        "risky": "Riskli",
        "safe": "Güvenli",
        "low_risk": "Düşük risk",
        "medium_risk": "Dikkat gerekli",
        "high_risk": "Yüksek risk",
        "yes": "Evet",
        "no": "Hayır",
        "footer_rows": "Temizlenmiş Veri Satırı",
        "footer_malicious": "Kötücül Oranı",
        "footer_note": "Destek amaçlıdır, kritik güvenlik kararlarında tek kaynak olarak kullanılmamalıdır.",
    },
    "EN": {
        "subtitle": "Check a link's risk quickly before opening it.",
        "analyze": "Analyze",
        "empty_url": "You need to enter a URL.",
        "model_missing": "Model files were not found. Run `python -m url_guard.train --base-dir .` first.",
        "safe_example": "Safe Example",
        "brand_spoof": "Brand Spoof",
        "shortener": "Shortener",
        "file_risk": "File Risk",
        "risky_status": "Potentially risky / malicious",
        "safe_status": "Probably safe",
        "risk_band": "Risk Band",
        "safe_probability": "Safe Probability",
        "threshold": "Threshold",
        "summary": "Summary",
        "anatomy": "Anatomy",
        "all_features": "All Features",
        "no_rule_note": "No extra rule note; the result comes from the model score.",
        "history": "History",
        "no_history": "No queries yet.",
        "risky": "Risky",
        "safe": "Safe",
        "low_risk": "Low risk",
        "medium_risk": "Needs attention",
        "high_risk": "High risk",
        "yes": "Yes",
        "no": "No",
        "footer_rows": "Cleaned Data Rows",
        "footer_malicious": "Malicious Ratio",
        "footer_note": "For decision support only; it should not be the only source for critical security decisions.",
    },
}

NOTE_TRANSLATIONS = {
    "URL teknik olarak geçerli görünmüyor.": "The URL does not look technically valid.",
    "Marka adı gerçek alan adı dışında kullanılmış.": "A brand name is used outside the real domain name.",
    "Marka adı URL içinde geçiyor ama ana alan adı o marka değil.": "A brand name appears in the URL, but the main domain is not that brand.",
    "Alan adı yerine IP adresi kullanılmış.": "An IP address is used instead of a domain name.",
    "@ işareti host bilgisini yanıltıcı gösterebilir.": "The @ symbol can make the host information misleading.",
    "URL kısaltıcı gerçek hedefi gizlediği için temkinli işaretlendi.": "The URL shortener was marked cautiously because it can hide the real target.",
    "Bilinen markanın kendi ana alan adı gibi görünüyor.": "It looks like the known brand's own main domain.",
}

FEATURE_LABELS_TR = {
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

FEATURE_LABELS_EN = {
    "url_length": "URL Length",
    "hostname_length": "Domain Length",
    "path_length": "Path Length",
    "path_length_no_slash": "Path Length Without Slashes",
    "query_length": "Query Length",
    "num_dots": "Number Of Dots",
    "num_hyphens": "Number Of Hyphens",
    "num_underscores": "Number Of Underscores",
    "num_slashes": "Number Of Slashes",
    "num_digits": "Number Of Digits In URL",
    "num_params": "Number Of Parameters",
    "num_fragments": "Number Of Fragment Marks",
    "num_at_symbols": "Number Of @ Signs",
    "num_equals": "Number Of Equal Signs",
    "num_ampersands": "Number Of Ampersands",
    "num_percent": "Number Of Percent Signs",
    "num_subdomains": "Number Of Subdomains",
    "subdomain_depth": "Subdomain Depth",
    "has_ip": "Uses IP Address",
    "has_at_symbol": "Contains @ Sign",
    "has_double_slash": "Has Extra Double Slash",
    "has_www": "Starts With WWW",
    "has_port": "Uses Custom Port",
    "port_number": "Port Number",
    "has_hex_encoding": "Contains Encoded Characters",
    "has_punycode": "Contains Punycode",
    "is_shortened": "Is URL Shortener",
    "has_suspicious_tld": "Suspicious Extension",
    "has_trusted_tld": "Trusted Extension",
    "is_net_tld": "Uses .net Extension",
    "is_edu_tld": "Education Domain Extension",
    "has_abused_country_tld": "Risky Country Extension",
    "tld_length": "Extension Length",
    "url_entropy": "URL Complexity Score",
    "domain_entropy": "Domain Complexity Score",
    "domain_core_entropy": "Main Domain Complexity Score",
    "domain_core_length": "Main Domain Length",
    "digit_ratio": "Digit Ratio",
    "letter_ratio": "Letter Ratio",
    "special_char_ratio": "Special Character Ratio",
    "vowel_ratio": "Vowel Ratio",
    "num_tokens": "Number Of Parts",
    "avg_token_length": "Average Part Length",
    "max_token_length": "Longest Part Length",
    "max_consecutive_digits": "Longest Consecutive Digits",
    "num_suspicious_keywords": "Suspicious Keyword Count",
    "has_suspicious_keywords": "Contains Suspicious Keywords",
    "brand_in_url": "Brand Name In URL",
    "brand_in_subdomain": "Brand Name In Subdomain",
    "brand_in_path": "Brand Name In Path",
    "url_depth": "URL Path Depth",
    "effective_url_depth": "Cleaned Path Depth",
    "trailing_slash": "Has Trailing Slash",
    "is_root_path": "Is Home Page Path",
    "domain_has_digits": "Domain Contains Digits",
    "has_exec_extension": "Executable File Extension",
    "has_script_extension": "Script File Extension",
    "is_valid_url": "Valid URL",
}

FEATURE_HINTS_TR = {
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

FEATURE_HINTS_EN = {
    "url_length": "Total character count of the canonical URL.",
    "hostname_length": "Length of the domain, also called the host section.",
    "path_length": "Character length of the path after the domain.",
    "query_length": "Length of the parameter section after the question mark.",
    "num_dots": "Total number of dot characters in the URL.",
    "num_hyphens": "Shows how many hyphens are used in the URL.",
    "num_digits": "Total number of digits in the URL text.",
    "num_params": "Estimated number of parameters in the query section.",
    "num_subdomains": "Number of subdomains to the left of the main domain.",
    "subdomain_depth": "Shows how deep the subdomain structure is.",
    "has_ip": "Shows whether an IP address is used instead of a domain name.",
    "has_at_symbol": "The @ sign can be used in some URLs to hide or confuse the real host.",
    "has_double_slash": "Shows extra double slash usage outside the scheme.",
    "has_www": "Shows whether the domain starts with www.",
    "has_port": "Shows whether the URL uses a non-default port.",
    "port_number": "The port number used in the URL, if present.",
    "has_hex_encoding": "Shows whether the URL contains hidden characters through percent encoding.",
    "has_punycode": "Shows punycode format used in internationalized domain names.",
    "is_shortened": "Shows whether the URL comes through a URL shortening service.",
    "has_suspicious_tld": "Shows whether the extension is in a frequently abused list.",
    "has_trusted_tld": "Shows whether the extension is in a common trusted group.",
    "is_edu_tld": "Shows whether the domain has an education-related extension.",
    "url_entropy": "Measures whether the URL looks random or complex.",
    "domain_entropy": "Shows character complexity of the domain section.",
    "domain_core_entropy": "Shows character complexity of the main domain label.",
    "digit_ratio": "Ratio of digits to all characters in the URL.",
    "letter_ratio": "Ratio of letters to all characters in the URL.",
    "special_char_ratio": "Ratio of non-letter and non-digit characters.",
    "num_suspicious_keywords": "Number of suspicious words detected in the URL.",
    "has_suspicious_keywords": "Shows whether the URL contains words like login, verify, or account.",
    "brand_in_url": "Shows whether a brand name appears in the URL.",
    "brand_in_subdomain": "Shows whether a brand name appears in the subdomain.",
    "brand_in_path": "Shows whether a brand name appears in the path.",
    "url_depth": "Shows how many parts the path section contains.",
    "is_root_path": "Shows whether the URL goes directly to the home page.",
    "domain_has_digits": "Shows whether the main domain contains digits.",
    "has_exec_extension": "Shows whether the URL ends with a risky extension such as exe, zip, or msi.",
    "has_script_extension": "Shows whether the URL ends with a script extension such as php or asp.",
    "is_valid_url": "Shows whether the URL can be technically parsed as valid.",
}

DEFAULT_FEATURE_HINTS = {
    "TR": "Bu değer URL'nin yapısından çıkarılan model girdilerinden biridir.",
    "EN": "This value is one of the model inputs extracted from the URL structure.",
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


def feature_label(key, lang):
    labels = FEATURE_LABELS_EN if lang == "EN" else FEATURE_LABELS_TR
    return labels.get(key, key.replace("_", " ").capitalize())


def feature_hint(key, lang):
    hints = FEATURE_HINTS_EN if lang == "EN" else FEATURE_HINTS_TR
    return hints.get(key, DEFAULT_FEATURE_HINTS[lang])


def feature_value(key, val, lang):
    if key in BINARY_FEATURES:
        return t("yes", lang) if int(val) == 1 else t("no", lang)
    if isinstance(val, float):
        return f"{val:.6f}" if abs(val) < 1 else f"{val:.4f}"
    return str(val)


try:
    payload, scaler = cached_artifacts()
except FileNotFoundError:
    lang_for_error = st.session_state.get("language", "TR")
    st.error(t("model_missing", lang_for_error))
    st.stop()

metrics_path = os.path.join(BASE_DIR, "models", "metrics.json")
metrics_mtime = os.path.getmtime(metrics_path) if os.path.exists(metrics_path) else 0
metrics = cached_metrics(metrics_mtime)

if "url_input" not in st.session_state:
    st.session_state.url_input = ""
if "history" not in st.session_state:
    st.session_state.history = []
if "last_prediction" not in st.session_state:
    st.session_state.last_prediction = None
if "pending_example_url" in st.session_state:
    st.session_state.url_input = st.session_state.pop("pending_example_url")

_, language_col = st.columns([0.78, 0.22])
with language_col:
    language = st.radio("Dil / Language", ["TR", "EN"], horizontal=True, label_visibility="collapsed", key="language")

st.markdown(
    f"""
<div class="hero">
  <div class="title">Malicious URL Guard</div>
  <div class="subtitle">{html.escape(t("subtitle", language))}</div>
</div>
""",
    unsafe_allow_html=True,
)

examples = {
    t("safe_example", language): "https://google.com",
    t("brand_spoof", language): "https://paypal.security-check.example.com/login",
    t("shortener", language): "https://bit.ly/abc123",
    t("file_risk", language): "https://example.com/download/invoice.exe",
}

main_col, side_col = st.columns([1.4, .6], gap="large")

with main_col:
    with st.form("analysis_form"):
        url_input = st.text_input("URL", key="url_input", placeholder="https://example.com/login?token=123")
        analyze = st.form_submit_button(t("analyze", language), type="primary", use_container_width=True)
    example_cols = st.columns(len(examples), gap="medium")
    for col, (label, value) in zip(example_cols, examples.items()):
        if col.button(label, use_container_width=True):
            st.session_state.pending_example_url = value
            st.rerun()

    if analyze:
        if not url_input.strip():
            st.warning(t("empty_url", language))
        else:
            prediction = predict_url(url_input, payload, scaler)
            st.session_state.last_prediction = prediction
            add_history(prediction)

    prediction = st.session_state.last_prediction
    if prediction:
        risk_pct = prediction.probability_malicious * 100
        band, risk_color = risk_band(prediction.probability_malicious, language)
        status_text = t("risky_status", language) if prediction.label else t("safe_status", language)
        quick_items = [
            (t("risk_band", language), band),
            (t("safe_probability", language), fmt_pct(prediction.probability_safe)),
            (t("threshold", language), fmt_pct(prediction.threshold)),
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

        tab_summary, tab_anatomy, tab_features = st.tabs([t("summary", language), t("anatomy", language), t("all_features", language)])
        with tab_summary:
            if prediction.notes:
                for note in prediction.notes:
                    st.markdown(f'<div class="note">{html.escape(translate_note(note, language))}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="empty-state">{html.escape(t("no_rule_note", language))}</div>', unsafe_allow_html=True)

        with tab_anatomy:
            anatomy = [
                (feature_label("hostname_length", language), prediction.features.get("hostname_length", 0), feature_hint("hostname_length", language)),
                (feature_label("path_length", language), prediction.features.get("path_length", 0), feature_hint("path_length", language)),
                (feature_label("query_length", language), prediction.features.get("query_length", 0), feature_hint("query_length", language)),
                (feature_label("subdomain_depth", language), prediction.features.get("subdomain_depth", 0), feature_hint("subdomain_depth", language)),
                (feature_label("num_suspicious_keywords", language), prediction.features.get("num_suspicious_keywords", 0), feature_hint("num_suspicious_keywords", language)),
                (feature_label("url_length", language), prediction.features.get("url_length", 0), feature_hint("url_length", language)),
                (feature_label("has_ip", language), t("yes", language) if prediction.features.get("has_ip", 0) else t("no", language), feature_hint("has_ip", language)),
                (feature_label("is_shortened", language), t("yes", language) if prediction.features.get("is_shortened", 0) else t("no", language), feature_hint("is_shortened", language)),
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
                val_text = feature_value(key, val, language)
                hint = feature_hint(key, language)
                chips.append(
                    f'<div class="feature-chip" title="{html.escape(hint, quote=True)}"><div class="feature-name">{html.escape(feature_label(key, language))}</div>'
                    f'<div class="feature-val">{html.escape(val_text)}</div></div>'
                )
            chips.append("</div>")
            st.markdown("".join(chips), unsafe_allow_html=True)

with side_col:
    st.markdown(f'<div class="panel"><div class="panel-title centered">{html.escape(t("history", language))}</div>', unsafe_allow_html=True)
    if st.session_state.history:
        st.markdown('<div class="history-list">', unsafe_allow_html=True)
        for item in st.session_state.history:
            status = t("risky", language) if item["label"] else t("safe", language)
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
        st.markdown(f'<div class="empty-state">{html.escape(t("no_history", language))}</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f"""
<div class="bottom-info">
  <span><strong>{html.escape(t("footer_rows", language))}:</strong> {int(metrics.get("rows", 0)):,}</span>
  <span><strong>{html.escape(t("footer_malicious", language))}:</strong> {metrics.get("malicious_ratio", 0):.4f}</span>
  <span><strong>Accuracy:</strong> {metrics.get("accuracy", 0):.4f}</span>
  <span><strong>Precision:</strong> {metrics.get("precision", 0):.4f}</span>
  <span><strong>Recall:</strong> {metrics.get("recall", 0):.4f}</span>
  <span><strong>F1:</strong> {metrics.get("f1", 0):.4f}</span>
  <span><strong>ROC-AUC:</strong> {metrics.get("roc_auc", 0):.4f}</span>
  <span><strong>PR-AUC:</strong> {metrics.get("pr_auc", 0):.4f}</span>
  <span>{html.escape(t("footer_note", language))}</span>
</div>
""",
    unsafe_allow_html=True,
)
