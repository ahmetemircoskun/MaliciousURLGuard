import html
import os
import sys

import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from url_guard.inference import load_artifacts, predict_url


st.set_page_config(page_title="Malicious URL Guard", page_icon="🛡️", layout="centered")

st.markdown(
    """
<style>
.stApp { background: #0f172a; color: #f8fafc; }
#MainMenu, footer, header { visibility: hidden; }
.block-container { max-width: 900px; padding-top: 2rem; }
.title { text-align: center; font-size: 2rem; font-weight: 750; }
.subtitle { text-align: center; color: #b6c2d6; margin: .35rem 0 1.2rem; }
.note { color: #cbd5e1; font-size: .9rem; }
.feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(210px, 1fr)); gap: .55rem; }
.feature-chip { border: 1px solid rgba(148, 163, 184, .22); border-radius: 8px; padding: .55rem .65rem; background: rgba(15, 23, 42, .72); }
.feature-name { color: #94a3b8; font-size: .76rem; }
.feature-val { color: #f8fafc; font-size: .92rem; font-weight: 650; overflow-wrap: anywhere; }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def cached_artifacts():
    return load_artifacts(BASE_DIR)


st.markdown('<div class="title">Malicious URL Guard</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">URL yapısını, alan adını ve taklit sinyallerini birlikte okuyan risk analizi</div>', unsafe_allow_html=True)

try:
    payload, scaler = cached_artifacts()
except FileNotFoundError:
    st.error("Model dosyaları bulunamadı. Önce `python -m url_guard.train --base-dir .` komutunu çalıştırın.")
    st.stop()

url_input = st.text_input("URL", placeholder="https://example.com/login?token=123")
analyze = st.button("Analiz et", type="primary")

if analyze:
    if not url_input.strip():
        st.warning("Bir URL girmen gerekiyor.")
    else:
        prediction = predict_url(url_input, payload, scaler)
        if prediction.label:
            st.error(f"Riskli / kötücül olabilir: %{prediction.probability_malicious * 100:.2f}")
        else:
            st.success(f"Muhtemelen güvenli: %{prediction.probability_safe * 100:.2f}")

        c1, c2, c3 = st.columns(3)
        c1.metric("Güvenli", f"%{prediction.probability_safe * 100:.2f}")
        c2.metric("Riskli", f"%{prediction.probability_malicious * 100:.2f}")
        c3.metric("Eşik", f"%{prediction.threshold * 100:.0f}")

        st.caption(f"Kanonik URL: `{prediction.canonical_url}`")
        if prediction.notes:
            st.markdown("#### Öne çıkan nedenler")
            for note in prediction.notes:
                st.markdown(f'<div class="note">- {html.escape(note)}</div>', unsafe_allow_html=True)

        st.markdown("#### Özellik değerleri")
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
