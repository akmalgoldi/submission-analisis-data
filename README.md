# E-Commerce Public Dataset Analysis & Dashboard

Proyek analisis data end-to-end menggunakan E-Commerce Public Dataset. Proyek ini mencakup analisis segmentasi pelanggan menggunakan metode RFM (Recency, Frequency, Monetary) serta analisis efisiensi pengiriman (logistik) secara geospasial. Proyek dideploy menggunakan Streamlit Dashboard interaktif.

## Struktur Direktori

```plaintext
submission/
├───dashboard/
│   ├───main_data.csv          # Dataset yang sudah dibersihkan (last 12 months)
│   └───dashboard.py           # Kode aplikasi Streamlit
├───data/
│   └───*.csv                  # Berkas .csv asli E-Commerce Public Dataset
├───notebook.ipynb             # Berkas analisis utama (sudah di-Run All)
├───README.md                  # Penjelasan cara run dashboard ini
├───requirements.txt           # Library dependencies yang digunakan
└───url.txt                    # Tautan aplikasi yang dideploy di Streamlit Cloud
```

## Persyaratan (Requirements)

Pastikan Anda memiliki Python 3.8 atau versi di atasnya terinstal di sistem Anda.

## Cara Menjalankan Dashboard Secara Lokal

### 1. Masuk ke direktori proyek:
```bash
cd submission
```

### 2. Buat Virtual Environment (Opsional tetapi disarankan):
- **Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```
- **macOS/Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### 3. Instal semua dependensi yang diperlukan:
```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi Streamlit:
```bash
streamlit run dashboard/dashboard.py
```

Dashboard akan otomatis terbuka pada peramban (browser) default Anda di alamat `http://localhost:8501`.
