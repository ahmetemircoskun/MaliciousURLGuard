import html
import json
import os
import sys

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
.stApp {
    background:
        radial-gradient(circle at top left, rgba(20, 184, 166, .18), transparent 32rem),
        linear-gradient(135deg, #08111f 0%, #101827 48%, #16151f 100%);
    color: #f8fafc;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 1120px; padding-top: 2rem; padding-bottom: 2rem; }
.hero {
    border: 1px solid rgba(148, 163, 184, .22);
    background: rgba(8, 17, 31, .72);
    border-radius: 8px;
    padding: 1.25rem 1.35rem;
    margin-bottom: 1rem;
    box-shadow: 0 18px 60px rgba(0, 0, 0, .26);
}
.eyebrow { color: #5eead4; font-size: .78rem; font-weight: 760; letter-spacing: 0; }
.title { font-size: 2.25rem; line-height: 1.05; font-weight: 820; margin-top: .25rem; }
.subtitle { color: #b6c2d6; margin-top: .5rem; max-width: 760px; }
.metric-row { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: .7rem; margin: .85rem 0; }
.metric-card {
    border: 1px solid rgba(148, 163, 184, .22);
    border-radius: 8px;
    background: rgba(15, 23, 42, .78);
    padding: .8rem .9rem;
}
.metric-label { color: #94a3b8; font-size: .78rem; }
.metric-value { color: #f8fafc; font-size: 1.35rem; font-weight: 780; margin-top: .15rem; }
.result-card {
    border: 1px solid rgba(148, 163, 184, .24);
    border-radius: 8px;
    background: rgba(15, 23, 42, .82);
    padding: 1rem;
    margin-top: 1rem;
}
.risk-title { font-size: 1.15rem; font-weight: 760; margin-bottom: .45rem; }
.risk-track { height: 12px; background: #1e293b; border-radius: 999px; overflow: hidden; border: 1px solid rgba(148, 163, 184, .16); }
.risk-fill { height: 100%; border-radius: 999px; }
.risk-meta { color: #cbd5e1; font-size: .88rem; margin-top: .55rem; overflow-wrap: anywhere; }
.note { color: #cbd5e1; font-size: .9rem; padding: .35rem 0; }
.section-title { color: #f8fafc; font-weight: 760; margin: 1.1rem 0 .6rem; }
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: .55rem; }
.feature-chip {
    border: 1px solid rgba(148, 163, 184, .20);
    border-radius: 8px;
    padding: .58rem .65rem;
    background: rgba(2, 6, 23, .46);
    min-height: 70px;
}
.feature-name { color: #94a3b8; font-size: .74rem; overflow-wrap: anywhere; }
.feature-val { color: #f8fafc; font-size: .9rem; font-weight: 680; overflow-wrap: anywhere; margin-top: .25rem; }
.stTextInput input {
    background: rgba(15, 23, 42, .92);
    border: 1px solid rgba(148, 163, 184, .28);
    color: #f8fafc;
}
.stButton > button {
    border-radius: 8px;
    min-height: 2.7rem;
    font-weight: 720;
}
@media (max-width: 720px) {
    .title { font-size: 1.75rem; }
    .metric-row { grid-template-columns: 1fr; }
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


st.markdown(
    """
<div class="hero">
  <div class="eyebrow">URL RISK ANALYSIS</div>
  <div class="title">Malicious URL Guard</div>
  <div class="subtitle">Alan adı, path, query, marka taklidi ve model skorunu birlikte okuyarak URL için açıklanabilir risk tahmini üretir.</div>
</div>
""",
    unsafe_allow_html=True,
)

try:
    payload, scaler = cached_artifacts()
except FileNotFoundError:
    st.error("Model dosyaları bulunamadı. Önce `python -m url_guard.train --base-dir .` komutunu çalıştırın.")
    st.stop()

metrics = cached_metrics()
st.markdown(
    f"""
<div class="metric-row">
  <div class="metric-card"><div class="metric-label">Test ROC-AUC</div><div class="metric-value">{metrics.get("roc_auc", 0):.3f}</div></div>
  <div class="metric-card"><div class="metric-label">Precision</div><div class="metric-value">{metrics.get("precision", 0):.3f}</div></div>
  <div class="metric-card"><div class="metric-label">Temiz veri</div><div class="metric-value">{int(metrics.get("rows", 0)):,}</div></div>
</div>
""",
    unsafe_allow_html=True,
)

examples = {
    "Google": "https://google.com",
    "Marka taklidi": "https://paypal.security-check.example.com/login",
    "Kısaltıcı": "https://bit.ly/abc123",
    "Dosya riski": "https://example.com/download/invoice.exe",
}

if "url_input" not in st.session_state:
    st.session_state.url_input = ""

example_cols = st.columns(len(examples))
for col, (label, value) in zip(example_cols, examples.items()):
    if col.button(label, use_container_width=True):
        st.session_state.url_input = value

with st.form("analysis_form"):
    url_input = st.text_input("URL", key="url_input", placeholder="https://example.com/login?token=123")
    analyze = st.form_submit_button("Analiz et", type="primary", use_container_width=True)

if analyze:
    if not url_input.strip():
        st.warning("Bir URL girmen gerekiyor.")
    else:
        prediction = predict_url(url_input, payload, scaler)
        risk_pct = prediction.probability_malicious * 100
        safe_pct = prediction.probability_safe * 100
        risk_color = "#fb7185" if prediction.label else "#2dd4bf"
        status_text = "Riskli / kötücül olabilir" if prediction.label else "Muhtemelen güvenli"

        st.markdown(
            f"""
<div class="result-card">
  <div class="risk-title">{html.escape(status_text)} · %{risk_pct:.2f}</div>
  <div class="risk-track"><div class="risk-fill" style="width: {risk_pct:.2f}%; background: {risk_color};"></div></div>
  <div class="risk-meta">Güvenli olasılığı: %{safe_pct:.2f} · Eşik: %{prediction.threshold * 100:.0f}</div>
  <div class="risk-meta">Kanonik URL: {html.escape(prediction.canonical_url)}</div>
</div>
""",
            unsafe_allow_html=True,
        )

        if prediction.label:
            st.error(f"Riskli / kötücül olabilir: %{prediction.probability_malicious * 100:.2f}")
        else:
            st.success(f"Muhtemelen güvenli: %{prediction.probability_safe * 100:.2f}")

        if prediction.notes:
            st.markdown('<div class="section-title">Öne çıkan nedenler</div>', unsafe_allow_html=True)
            for note in prediction.notes:
                st.markdown(f'<div class="note">- {html.escape(note)}</div>', unsafe_allow_html=True)

        st.markdown('<div class="section-title">Özellik değerleri</div>', unsafe_allow_html=True)
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

st.caption("Bu araç karar destek amaçlıdır; güvenlik açısından kritik kararlarda tek başına kullanılmamalıdır.")
