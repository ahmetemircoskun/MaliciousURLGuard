# Malicious URL Guard

Malicious URL Guard, URL'lerin güvenli mi yoksa phishing, malware veya defacement gibi riskli bir örüntüye mi benzediğini tahmin eden bir makine öğrenmesi projesidir.

Uygulama URL'yi tek bir tutarlı forma çevirir, alan adı ve URL yapısından özellikler çıkarır, eğitilmiş modelle risk skorunu hesaplar ve sonucu Streamlit arayüzünde gösterir.

> Bu proje karar destek amaçlıdır. Kritik güvenlik kararlarında tek başına kesin kanıt olarak kullanılmamalıdır.

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
