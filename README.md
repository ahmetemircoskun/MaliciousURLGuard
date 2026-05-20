# Malicious URL Guard

Malicious URL Guard, bir URL'nin güvenli mi yoksa phishing, malware veya defacement gibi kötücül bir örüntüye mi benzediğini tahmin eden bir makine öğrenmesi projesidir. Proje ham URL'yi önce temiz ve tutarlı bir forma çevirir, URL yapısından sayısal özellikler çıkarır, eğitilmiş modelle risk skorunu hesaplar ve sonucu Streamlit arayüzünde gösterir.

Bu araç karar destek amaçlıdır. Güvenlik açısından kritik bir kararda tek başına kesin kanıt olarak kullanılmamalıdır.

## Proje Yapısı

| Yol | Açıklama |
| --- | --- |
| `app/main.py` | Streamlit tabanlı kullanıcı arayüzü. |
| `src/url_guard/` | URL temizleme, özellik çıkarma, eğitim ve tahmin kodları. |
| `src/1_Data_Preprocessing.ipynb` | Veri temizleme akışını anlatan notebook. |
| `src/2_Model_Training.ipynb` | Model eğitim akışını anlatan notebook. |
| `data/raw/` | Ham veri dosyasının yerel olarak konacağı klasör. |
| `data/processed/cleaned_dataset.csv` | Temizlenmiş ve tekilleştirilmiş eğitim verisi. |
| `data/processed/confusion_matrix.png` | Son eğitimden üretilen karmaşıklık matrisi. |
| `data/processed/roc_curve.png` | Son eğitimden üretilen ROC eğrisi. |
| `data/processed/precision_recall_curve.png` | Son eğitimden üretilen precision-recall eğrisi. |
| `models/best_model.joblib` | Eğitilmiş model, özellik sırası, eşik ve metrik bilgileri. |
| `models/scaler.joblib` | Eğitimde kullanılan ölçekleyici. |
| `models/metrics.json` | Son eğitim metrikleri. |
| `tests/` | Temel doğrulama testleri. |

## Dataset

Ham veri Kaggle üzerindeki Malicious URLs Dataset kaynağından alınır:

[https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset)

Telif ve dağıtım açısından ham CSV repoya eklenmez. Dosyayı Kaggle'dan indirip şu konuma koymak yeterlidir:

```text
data/raw/malicious_phish.csv
```

## Kurulum

macOS veya Linux:

```bash
cd /Users/aecoskun/Desktop/MaliciousURLGuard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows:

```bat
cd C:\path\to\MaliciousURLGuard
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uygulamayı Çalıştırma

macOS veya Linux:

```bash
./run.sh
```

Windows:

```bat
run.bat
```

Elle çalıştırmak istersen:

```bash
PYTHONPATH=src .venv/bin/streamlit run app/main.py
```

Windows için eşdeğeri:

```bat
set PYTHONPATH=src
.venv\Scripts\streamlit run app\main.py
```

## Modeli Yeniden Eğitme

```bash
PYTHONPATH=src MPLCONFIGDIR=.mplconfig .venv/bin/python -m url_guard.train --base-dir .
```

Windows:

```bat
set PYTHONPATH=src
.venv\Scripts\python -m url_guard.train --base-dir .
```

Eğitim tamamlandığında `data/processed/` altındaki CSV ve grafikler, `models/` altındaki model dosyaları ve `metrics.json` güncellenir.

## Son Eğitim Metrikleri

| Metrik | Değer |
| --- | ---: |
| Temizlenmiş Veri Satırı | 622,784 |
| Kötücül oranı | 0.3358 |
| Accuracy | 0.9184 |
| Precision | 0.9318 |
| Recall | 0.8168 |
| F1 | 0.8705 |
| ROC-AUC | 0.9690 |
| PR-AUC | 0.9523 |

`confusion_matrix.png`, `roc_curve.png` ve `precision_recall_curve.png` dosyaları son model eğitimiyle aynı anda üretilmiştir. Bu grafikler modelin test setindeki genel davranışını hızlı kontrol etmek için tutulur.

## Test

```bash
PYTHONPATH=src .venv/bin/pytest -q
```

Windows:

```bat
set PYTHONPATH=src
.venv\Scripts\pytest -q
```
