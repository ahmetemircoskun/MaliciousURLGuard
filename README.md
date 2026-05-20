# Malicious URL Guard

<details open>
<summary>[TR] Türkçe</summary>

Malicious URL Guard, URL'lerin güvenli mi yoksa phishing, malware veya defacement gibi riskli bir örüntüye mi benzediğini tahmin eden bir makine öğrenmesi projesidir.

Uygulama URL'yi tek bir tutarlı forma çevirir, alan adı ve URL yapısından özellikler çıkarır, eğitilmiş modelle risk skorunu hesaplar ve sonucu Streamlit arayüzünde gösterir.

> Bu proje karar destek amaçlıdır. Kritik güvenlik kararlarında tek başına kesin kanıt olarak kullanılmamalıdır.

Arayüz Türkçe ve İngilizce dil seçeneğiyle kullanılabilir. Dil değiştirildiğinde sonuç metinleri, geçmiş, sekmeler, özellik adları ve açıklamaları seçilen dile göre güncellenir.

## Proje Yapısı

| Yol | Açıklama |
| --- | --- |
| `app/main.py` | Streamlit arayüzü. |
| `src/url_guard/` | URL ayrıştırma, özellik çıkarma, eğitim ve tahmin kodları. |
| `src/1_Data_Preprocessing.ipynb` | Veri temizleme akışını anlatan notebook. |
| `src/2_Model_Training.ipynb` | Model eğitim akışını anlatan notebook. |
| `data/raw/` | Ham datasetin yerel olarak konacağı klasör. |
| `data/processed/cleaned_dataset.csv` | Temizlenmiş ve tekilleştirilmiş dataset. |
| `data/processed/*.png` | Eğitimden çıkan metrik grafikleri. |
| `models/best_model.joblib` | Eğitilmiş model, özellik sırası, eşik ve metrik bilgileri. |
| `models/scaler.joblib` | Eğitimde kullanılan ölçekleyici. |
| `models/metrics.json` | Son eğitim metrikleri. |
| `tests/` | Temel doğrulama testleri. |

## Dataset

Processed dataset bu repoda bulunur:

- İşlenmiş veri: `data/processed/cleaned_dataset.csv`

Ham dataset telif/dağıtım riski oluşturmamak için repoda tutulmaz. Kaynak dataset Kaggle üzerindedir:

[Kaggle - Malicious URLs Dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset)

Modeli veya processed dataset'i yeniden üretmek için Kaggle'dan `malicious_phish.csv` dosyasını indirip şu konuma koyun:

```text
data/raw/malicious_phish.csv
```

Eğitim hattı, public repoya uygun olmayan secret formatlı URL parametrelerini satır seviyesinde filtreler ve processed dataset'i yeniden oluşturur.

## Kurulum

### macOS / Linux

```bash
cd /path/to/MaliciousURLGuard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows

```bat
cd C:\path\to\MaliciousURLGuard
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Uygulamayı Çalıştırma

### macOS / Linux

```bash
./run.sh
```

### Windows

```bat
run.bat
```

## Manuel Çalıştırma

### macOS / Linux

```bash
PYTHONPATH=src .venv/bin/streamlit run app/main.py
```

### Windows

```bat
set PYTHONPATH=src
.venv\Scripts\streamlit run app\main.py
```

## Dataseti Yeniden Oluşturma

Ham dataset dosyası `data/raw/malicious_phish.csv` konumundayken aşağıdaki komut eğitim hattını baştan çalıştırır. Bu işlem:

- `data/processed/cleaned_dataset.csv` dosyasını yeniden üretir.
- `data/processed/confusion_matrix.png` dosyasını günceller.
- `data/processed/roc_curve.png` dosyasını günceller.
- `data/processed/precision_recall_curve.png` dosyasını günceller.
- `models/` altındaki model, scaler ve metrik dosyalarını günceller.

### macOS / Linux

```bash
PYTHONPATH=src MPLCONFIGDIR=.mplconfig .venv/bin/python -m url_guard.train --base-dir .
```

### Windows

```bat
set PYTHONPATH=src
.venv\Scripts\python -m url_guard.train --base-dir .
```

## Test

### macOS / Linux

```bash
PYTHONPATH=src .venv/bin/pytest -q
```

### Windows

```bat
set PYTHONPATH=src
.venv\Scripts\pytest -q
```

## Son Eğitim Metrikleri

| Metrik | Değer |
| --- | ---: |
| Temizlenmiş Veri Satırı | 588,792 |
| Kötücül Oranı | 0.3339 |
| Accuracy | 0.9194 |
| Precision | 0.9323 |
| Recall | 0.8179 |
| F1 | 0.8714 |
| ROC-AUC | 0.9694 |
| PR-AUC | 0.9527 |

## Notlar

- Raw dataset repoda tutulmaz; Kaggle'dan indirildikten sonra `data/raw/malicious_phish.csv` konumuna yerleştirilir.
- Processed dataset repoda tutulur.
- `data/raw/malicious_phish.original_local_backup.csv` sadece yerel yedektir ve git'e eklenmez.
- Model artifact dosyaları repoda hazır gelir; uygulamayı çalıştırmak için yeniden eğitim zorunlu değildir.

</details>

<details>
<summary>[EN] English</summary>

Malicious URL Guard is a machine learning project that estimates whether a URL looks safe or resembles risky patterns such as phishing, malware, or defacement.

The application canonicalizes the URL into a consistent form, extracts features from the domain and URL structure, calculates a risk score with a trained model, and shows the result in a Streamlit interface.

> This project is intended for decision support. It should not be used as the only proof for critical security decisions.

The interface supports Turkish and English. When the language is changed, result texts, history, tabs, feature names, and feature explanations are updated accordingly.

## Project Structure

| Path | Description |
| --- | --- |
| `app/main.py` | Streamlit interface. |
| `src/url_guard/` | URL parsing, feature extraction, training, and prediction code. |
| `src/1_Data_Preprocessing.ipynb` | Notebook describing the data cleaning flow. |
| `src/2_Model_Training.ipynb` | Notebook describing the model training flow. |
| `data/raw/` | Local folder for the raw dataset. |
| `data/processed/cleaned_dataset.csv` | Cleaned and deduplicated dataset. |
| `data/processed/*.png` | Metric charts generated during training. |
| `models/best_model.joblib` | Trained model, feature order, threshold, and metric metadata. |
| `models/scaler.joblib` | Scaler used during training. |
| `models/metrics.json` | Latest training metrics. |
| `tests/` | Basic validation tests. |

## Dataset

The processed dataset is included in this repository:

- Processed data: `data/processed/cleaned_dataset.csv`

The raw dataset is not stored in the repository to avoid redistribution/copyright risk. The source dataset is available on Kaggle:

[Kaggle - Malicious URLs Dataset](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset)

To rebuild the model or processed dataset, download `malicious_phish.csv` from Kaggle and place it here:

```text
data/raw/malicious_phish.csv
```

The training pipeline filters secret-shaped URL parameters at row level and recreates the processed dataset.

## Installation

### macOS / Linux

```bash
cd /path/to/MaliciousURLGuard
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows

```bat
cd C:\path\to\MaliciousURLGuard
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Running The App

### macOS / Linux

```bash
./run.sh
```

### Windows

```bat
run.bat
```

## Manual Run

### macOS / Linux

```bash
PYTHONPATH=src .venv/bin/streamlit run app/main.py
```

### Windows

```bat
set PYTHONPATH=src
.venv\Scripts\streamlit run app\main.py
```

## Rebuilding The Dataset

When the raw dataset is available at `data/raw/malicious_phish.csv`, the command below runs the full training pipeline again. This process:

- Recreates `data/processed/cleaned_dataset.csv`.
- Updates `data/processed/confusion_matrix.png`.
- Updates `data/processed/roc_curve.png`.
- Updates `data/processed/precision_recall_curve.png`.
- Updates the model, scaler, and metric files under `models/`.

### macOS / Linux

```bash
PYTHONPATH=src MPLCONFIGDIR=.mplconfig .venv/bin/python -m url_guard.train --base-dir .
```

### Windows

```bat
set PYTHONPATH=src
.venv\Scripts\python -m url_guard.train --base-dir .
```

## Test

### macOS / Linux

```bash
PYTHONPATH=src .venv/bin/pytest -q
```

### Windows

```bat
set PYTHONPATH=src
.venv\Scripts\pytest -q
```

## Latest Training Metrics

| Metric | Value |
| --- | ---: |
| Cleaned Data Rows | 588,792 |
| Malicious Ratio | 0.3339 |
| Accuracy | 0.9194 |
| Precision | 0.9323 |
| Recall | 0.8179 |
| F1 | 0.8714 |
| ROC-AUC | 0.9694 |
| PR-AUC | 0.9527 |

## Notes

- The raw dataset is not stored in the repository; after downloading it from Kaggle, place it at `data/raw/malicious_phish.csv`.
- The processed dataset is stored in the repository.
- `data/raw/malicious_phish.original_local_backup.csv` is only a local backup and is not tracked by git.
- Model artifact files are included, so retraining is not required to run the application.

</details>
