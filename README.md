# Malicious URL Guard - Yeniden Kurulmuş Sürüm

Bu proje, verilen bir URL'nin güvenli mi yoksa kötücül/phishing olma ihtimali yüksek mi olduğunu tahmin eder.
Eski projedeki ana problem, aynı URL temizleme ve özellik çıkarma mantığının notebook ile Streamlit uygulaması arasında kopyalanmış olmasıydı. Bu sürümde bütün kritik mantık `src/url_guard/` altında tek yerde duruyor; eğitim, test ve uygulama aynı kodu kullanıyor.

## Klasör yapısı

| Yol | Ne işe yarar? |
| --- | --- |
| `app/main.py` | Streamlit arayüzü. |
| `src/url_guard/` | URL temizleme, özellik çıkarma, eğitim ve tahmin kodları. |
| `src/1_Data_Preprocessing.ipynb` | Veriyi temizleme notebook'u; ana modülü çağırır. |
| `src/2_Model_Training.ipynb` | Model eğitim notebook'u; ana eğitim komutunu çağırır. |
| `data/raw/malicious_phish.csv` | Ham Kaggle verisi. |
| `data/processed/cleaned_dataset.csv` | Temizlenmiş ve tekilleştirilmiş veri. |
| `data/processed/*.png` | Eğitimden çıkan metrik grafikleri. |
| `models/best_model.joblib` | Kalibre edilmiş model, feature sırası, eşik ve metrikler. |
| `models/scaler.joblib` | Eğitimde kullanılan `StandardScaler`. |
| `models/metrics.json` | Son eğitim metriklerinin okunabilir hali. |
| `tests/` | Temel URL temizleme ve özellik testleri. |

## Bu sürümde ne düzeldi?

- Bozuk karakterli, kontrol karakteri içeren veya geçerli host üretmeyen URL'ler eğitimden atılıyor.
- `http`, `https`, default port ve gereksiz son slash farkları tek kanonik URL'ye indiriliyor.
- Özellik çıkarma artık hem eğitimde hem uygulamada aynı `extract_features` fonksiyonundan geliyor.
- Marka taklidi, IP kullanımı, `@` işareti ve URL kısaltıcılar için tahmin üstüne açıklanabilir kural katmanı var.
- Model metrikleri ve grafikler eğitim çıktısı olarak saklanıyor.
- Basit testler var; en azından en kritik URL normalize etme davranışları kırılırsa hemen yakalanıyor.

## Kurulum

```bash
cd /Users/aecoskun/Desktop/AI_URL_Guard_Yeni
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

Bu klasörde `.venv` zaten oluşturuldu; tekrar kurmak istersen komutlar yukarıda.

## Uygulamayı çalıştırma

```bash
cd /Users/aecoskun/Desktop/AI_URL_Guard_Yeni
PYTHONPATH=src .venv/bin/streamlit run app/main.py
```

## Modeli baştan üretme

```bash
cd /Users/aecoskun/Desktop/AI_URL_Guard_Yeni
PYTHONPATH=src MPLCONFIGDIR=.mplconfig .venv/bin/python -m url_guard.train --base-dir .
```

Son çalıştırmada çıkan metrikler:

| Metrik | Değer |
| --- | ---: |
| Satır sayısı | 622,784 |
| Accuracy | 0.9184 |
| Precision | 0.9318 |
| Recall | 0.8168 |
| F1 | 0.8705 |
| ROC-AUC | 0.9690 |
| PR-AUC | 0.9523 |

## Test

```bash
cd /Users/aecoskun/Desktop/AI_URL_Guard_Yeni
PYTHONPATH=src .venv/bin/pytest -q
```

## Kısa not

Bu araç güvenlik kararı için tek başına kanıt değildir. Amaç URL'yi hızlıca yapısal olarak okumak, açık taklit sinyallerini yakalamak ve modeli tutarlı bir veri hattıyla kullanmaktır.
