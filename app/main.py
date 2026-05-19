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
    --bg: #07111f;
    --panel: rgba(8, 18, 32, .78);
    --panel-strong: rgba(10, 24, 43, .94);
    --line: rgba(148, 163, 184, .24);
    --muted: #9fb0c7;
    --text: #f8fafc;
    --cyan: #2dd4bf;
    --blue: #38bdf8;
    --rose: #fb7185;
    --amber: #fbbf24;
}
.stApp {
    background:
        radial-gradient(circle at 14% 12%, rgba(45, 212, 191, .22), transparent 30rem),
        radial-gradient(circle at 92% 8%, rgba(56, 189, 248, .16), transparent 28rem),
        linear-gradient(135deg, #07111f 0%, #0d1b2f 45%, #151927 100%);
    color: var(--text);
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 1180px; padding-top: 1.25rem; padding-bottom: 2.25rem; }

.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: .85rem;
    margin-bottom: .9rem;
}
.brand-mark {
    display: flex;
    align-items: center;
    gap: .6rem;
    color: #dffcff;
    font-weight: 820;
}
.brand-dot {
    width: 34px;
    height: 34px;
    border-radius: 8px;
    display: grid;
    place-items: center;
    background: linear-gradient(135deg, rgba(45, 212, 191, .95), rgba(56, 189, 248, .82));
    color: #06111f;
    box-shadow: 0 0 26px rgba(45, 212, 191, .28);
}
.nav-pills {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-end;
    gap: .45rem;
}
.pill {
    border: 1px solid rgba(148, 163, 184, .20);
    border-radius: 999px;
    padding: .45rem .72rem;
    color: #cbd5e1;
    background: rgba(15, 23, 42, .48);
    font-size: .82rem;
}

.hero {
    position: relative;
    overflow: hidden;
    border: 1px solid var(--line);
    background:
        linear-gradient(145deg, rgba(8, 18, 32, .92), rgba(13, 32, 52, .76)),
        repeating-linear-gradient(90deg, rgba(148, 163, 184, .06) 0 1px, transparent 1px 72px);
    border-radius: 8px;
    padding: 1.45rem;
    box-shadow: 0 24px 80px rgba(0, 0, 0, .32);
}
.hero:after {
    content: "";
    position: absolute;
    right: -80px;
    top: -90px;
    width: 290px;
    height: 290px;
    border-radius: 999px;
    background: radial-gradient(circle, rgba(45, 212, 191, .24), transparent 66%);
    animation: pulseGlow 4.8s ease-in-out infinite;
}
@keyframes pulseGlow {
    0%, 100% { transform: scale(.95); opacity: .70; }
    50% { transform: scale(1.08); opacity: 1; }
}
.eyebrow { color: var(--cyan); font-size: .78rem; font-weight: 820; letter-spacing: 0; }
.title { font-size: clamp(2rem, 4vw, 4rem); line-height: .96; font-weight: 880; margin: .35rem 0 .65rem; max-width: 760px; }
.subtitle { color: #b6c2d6; max-width: 720px; line-height: 1.58; }
.hero-grid { display: grid; grid-template-columns: minmax(0, 1.35fr) minmax(280px, .65fr); gap: 1rem; align-items: stretch; }
.scanner-card {
    border: 1px solid rgba(45, 212, 191, .22);
    border-radius: 8px;
    background: rgba(2, 6, 23, .46);
    padding: .95rem;
    position: relative;
    z-index: 1;
}
.scanner-line {
    height: 5px;
    border-radius: 99px;
    background: linear-gradient(90deg, transparent, var(--cyan), var(--blue), transparent);
    animation: scanMove 2.8s linear infinite;
    margin: .75rem 0;
}
@keyframes scanMove {
    0% { transform: translateX(-32%); opacity: .45; }
    50% { opacity: 1; }
    100% { transform: translateX(32%); opacity: .45; }
}
.scanner-row { display: flex; justify-content: space-between; gap: .8rem; color: #cbd5e1; font-size: .86rem; padding: .35rem 0; border-bottom: 1px solid rgba(148, 163, 184, .12); }
.scanner-row:last-child { border-bottom: 0; }

.workbench {
    margin-top: 1rem;
    display: grid;
    grid-template-columns: minmax(0, 1.25fr) minmax(280px, .75fr);
    gap: 1rem;
}
.panel {
    border: 1px solid var(--line);
    border-radius: 8px;
    background: var(--panel);
    padding: 1rem;
    box-shadow: 0 16px 60px rgba(0, 0, 0, .20);
}
.panel-title { font-weight: 820; color: #eef8ff; margin-bottom: .25rem; }
.panel-subtitle { color: var(--muted); font-size: .9rem; margin-bottom: .8rem; }
.example-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: .5rem; margin-bottom: .75rem; }
.stButton > button {
    border-radius: 8px;
    min-height: 2.65rem;
    font-weight: 760;
    border: 1px solid rgba(148, 163, 184, .22);
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
.risk-head { display: flex; justify-content: space-between; gap: 1rem; align-items: flex-end; }
.risk-title { font-size: 1.35rem; font-weight: 840; }
.risk-score { font-size: 2.3rem; line-height: 1; font-weight: 900; }
.risk-track { height: 14px; background: #182235; border-radius: 999px; overflow: hidden; border: 1px solid rgba(148, 163, 184, .16); margin: .85rem 0 .6rem; }
.risk-fill { height: 100%; border-radius: 999px; box-shadow: 0 0 22px currentColor; }
.risk-meta { color: #cbd5e1; font-size: .9rem; overflow-wrap: anywhere; }
.signal-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .55rem; margin-top: .8rem; }
.signal-card { border: 1px solid rgba(148, 163, 184, .18); border-radius: 8px; padding: .7rem; background: rgba(2, 6, 23, .42); }
.signal-label { color: #94a3b8; font-size: .72rem; }
.signal-value { color: #f8fafc; font-size: 1rem; font-weight: 780; margin-top: .2rem; overflow-wrap: anywhere; }
.section-title { color: #f8fafc; font-weight: 800; margin: 1.05rem 0 .55rem; }
.note { color: #d8e3f2; font-size: .92rem; padding: .42rem .55rem; border-left: 2px solid var(--cyan); background: rgba(45, 212, 191, .07); margin-bottom: .35rem; }
.history-list { display: grid; gap: .55rem; }
.history-item { border: 1px solid rgba(148, 163, 184, .18); border-radius: 8px; background: rgba(2, 6, 23, .40); padding: .62rem .68rem; }
.history-url { color: #e2e8f0; font-size: .86rem; overflow-wrap: anywhere; }
.history-meta { color: #94a3b8; font-size: .76rem; margin-top: .18rem; }
.empty-state { color: #94a3b8; font-size: .9rem; border: 1px dashed rgba(148, 163, 184, .26); border-radius: 8px; padding: .85rem; }
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(176px, 1fr)); gap: .55rem; }
.feature-chip { border: 1px solid rgba(148, 163, 184, .18); border-radius: 8px; padding: .58rem .65rem; background: rgba(2, 6, 23, .38); min-height: 68px; }
.feature-name { color: #94a3b8; font-size: .72rem; overflow-wrap: anywhere; }
.feature-val { color: #f8fafc; font-size: .9rem; font-weight: 720; overflow-wrap: anywhere; margin-top: .25rem; }
.bottom-info {
    margin-top: 1.25rem;
    border: 1px solid rgba(148, 163, 184, .16);
    border-radius: 8px;
    background: rgba(2, 6, 23, .36);
    padding: .75rem .85rem;
    color: #9fb0c7;
    font-size: .82rem;
    display: flex;
    flex-wrap: wrap;
    gap: .7rem 1rem;
    justify-content: space-between;
}
.bottom-info strong { color: #cbd5e1; font-weight: 720; }

@media (max-width: 860px) {
    .topbar { align-items: flex-start; }
    .nav-pills { display: none; }
    .hero-grid, .workbench { grid-template-columns: 1fr; }
    .example-grid, .signal-grid { grid-template-columns: 1fr 1fr; }
    .risk-head { align-items: flex-start; flex-direction: column; }
}
@media (max-width: 560px) {
    .block-container { padding-left: .8rem; padding-right: .8rem; }
    .example-grid, .signal-grid { grid-template-columns: 1fr; }
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
        "time": datetime.now().strftime("%H:%M"),
        "url": prediction.raw_url,
        "canonical": prediction.canonical_url,
        "risk": prediction.probability_malicious,
        "label": prediction.label,
    }
    history = [item] + st.session_state.history
    st.session_state.history = history[:8]


def risk_band(probability):
    if probability >= 0.75:
        return "Yüksek risk", "#fb7185"
    if probability >= 0.55:
        return "Dikkat gerekli", "#fbbf24"
    return "Düşük risk", "#2dd4bf"


def fmt_pct(value):
    return f"%{value * 100:.2f}"


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

top_left, top_right = st.columns([1, 1])
with top_left:
    st.markdown(
        """
<div class="topbar">
  <div class="brand-mark"><div class="brand-dot">M</div><div>Malicious URL Guard</div></div>
</div>
""",
        unsafe_allow_html=True,
    )
with top_right:
    menu_cols = st.columns([1, 1, 1])
    with menu_cols[2]:
        with st.popover("☰ Menü", use_container_width=True):
            st.markdown("**Kısayollar**")
            st.caption("Örnekleri kullan, geçmiş sorguları incele veya modeli yeniden eğitmek için README adımlarını takip et.")
            if st.button("Geçmişi temizle", use_container_width=True):
                st.session_state.history = []
                st.session_state.last_prediction = None
                st.rerun()
            st.markdown("---")
            st.caption("Mobilde bu menü üstte kompakt kalır; paneller ekran genişliğine göre alta dizilir.")

st.markdown(
    """
<div class="hero">
  <div class="hero-grid">
    <div>
      <div class="eyebrow">STRUCTURAL URL DEFENSE</div>
      <div class="title">Şüpheli bağlantıları açmadan önce oku.</div>
      <div class="subtitle">Alan adı, alt alan, path, query, marka taklidi, kısaltıcı ve model skorunu tek ekranda birleştiren açıklanabilir URL risk analizi.</div>
    </div>
    <div class="scanner-card">
      <div class="scanner-row"><span>Lexical scanner</span><strong>active</strong></div>
      <div class="scanner-line"></div>
      <div class="scanner-row"><span>Brand impersonation</span><strong>watched</strong></div>
      <div class="scanner-row"><span>Structural signals</span><strong>mapped</strong></div>
      <div class="scanner-row"><span>Hybrid scoring</span><strong>ready</strong></div>
    </div>
  </div>
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

main_col, side_col = st.columns([1.35, .65], gap="large")

with main_col:
    st.markdown('<div class="panel"><div class="panel-title">URL analizi</div><div class="panel-subtitle">Bir bağlantı gir veya hazır senaryolardan biriyle risk motorunu dene.</div>', unsafe_allow_html=True)
    example_cols = st.columns(len(examples))
    for col, (label, value) in zip(example_cols, examples.items()):
        if col.button(label, use_container_width=True):
            st.session_state.url_input = value

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
        safe_pct = prediction.probability_safe * 100
        band, risk_color = risk_band(prediction.probability_malicious)
        status_text = "Riskli / kötücül olabilir" if prediction.label else "Muhtemelen güvenli"
        high_signals = [
            ("Risk bandı", band),
            ("Güvenli olasılığı", f"%{safe_pct:.2f}"),
            ("Model eşiği", f"%{prediction.threshold * 100:.0f}"),
            ("Alt alan derinliği", int(prediction.features.get("subdomain_depth", 0))),
            ("Şüpheli kelime", int(prediction.features.get("num_suspicious_keywords", 0))),
            ("URL uzunluğu", int(prediction.features.get("url_length", 0))),
        ]

        st.markdown(
            f"""
<div class="result-card">
  <div class="risk-head">
    <div>
      <div class="risk-title">{html.escape(status_text)}</div>
      <div class="risk-meta">Kanonik URL: {html.escape(prediction.canonical_url)}</div>
    </div>
    <div class="risk-score" style="color: {risk_color};">%{risk_pct:.2f}</div>
  </div>
  <div class="risk-track"><div class="risk-fill" style="width: {risk_pct:.2f}%; background: {risk_color}; color: {risk_color};"></div></div>
  <div class="signal-grid">
    {''.join(f'<div class="signal-card"><div class="signal-label">{html.escape(str(k))}</div><div class="signal-value">{html.escape(str(v))}</div></div>' for k, v in high_signals)}
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        tab_summary, tab_anatomy, tab_features = st.tabs(["Özet", "URL anatomisi", "Tüm özellikler"])
        with tab_summary:
            st.markdown('<div class="section-title">Öne çıkan nedenler</div>', unsafe_allow_html=True)
            if prediction.notes:
                for note in prediction.notes:
                    st.markdown(f'<div class="note">{html.escape(note)}</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="empty-state">Ek kural notu yok; karar ağırlıklı olarak model skorundan geliyor.</div>', unsafe_allow_html=True)

        with tab_anatomy:
            anatomy = [
                ("Host uzunluğu", prediction.features.get("hostname_length", 0)),
                ("Path uzunluğu", prediction.features.get("path_length", 0)),
                ("Query uzunluğu", prediction.features.get("query_length", 0)),
                ("Nokta sayısı", prediction.features.get("num_dots", 0)),
                ("Rakam oranı", f"{prediction.features.get('digit_ratio', 0):.4f}"),
                ("Entropy", f"{prediction.features.get('url_entropy', 0):.4f}"),
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
                if isinstance(val, float):
                    val_text = f"{val:.6f}" if abs(val) < 1 else f"{val:.4f}"
                else:
                    val_text = str(val)
                chips.append(
                    f'<div class="feature-chip"><div class="feature-name">{html.escape(key)}</div>'
                    f'<div class="feature-val">{html.escape(val_text)}</div></div>'
                )
            chips.append("</div>")
            st.markdown("".join(chips), unsafe_allow_html=True)

with side_col:
    st.markdown('<div class="panel"><div class="panel-title">Geçmiş sorgular</div><div class="panel-subtitle">Son analizler bu oturumda tutulur.</div>', unsafe_allow_html=True)
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
        st.markdown('<div class="empty-state">Henüz sorgu yok. Bir URL analiz edildiğinde burada görünecek.</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="panel" style="margin-top: 1rem;">
  <div class="panel-title">Risk panelleri</div>
  <div class="panel-subtitle">Skor yalnızca model çıktısı değildir; açık taklit sinyalleri kural katmanıyla tekrar değerlendirilir.</div>
  <div class="scanner-row"><span>Marka apex kontrolü</span><strong>on</strong></div>
  <div class="scanner-row"><span>IP / @ işareti</span><strong>on</strong></div>
  <div class="scanner-row"><span>Kısaltıcı domain</span><strong>on</strong></div>
  <div class="scanner-row"><span>Executable path</span><strong>on</strong></div>
</div>
""",
        unsafe_allow_html=True,
    )

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
