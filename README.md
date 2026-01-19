# Sistem Peringatan Dini Kebakaran Hutan Provinsi Riau

Aplikasi web profesional untuk sistem peringatan dini kebakaran hutan di Provinsi Riau menggunakan model machine learning Stacking Classifier.

## Fitur Utama

- Integrasi model ML Stacking Classifier (XGBoost + Random Forest) dengan regularisasi ketat
- Feature Engineering manual (X1, X2, X3)
- Booster probabilitas untuk threshold tinggi (0.64-0.81)
- Simulasi data dari Google Earth Engine (LST, NDVI, Curah Hujan)
- Antarmuka modern dengan Tailwind CSS
- Peta interaktif Leaflet JS dengan marker dinamis
- Panel notifikasi leveling (Danger/Warning/Safe)

## Struktur Proyek

```
.
├── app.py                 # Backend Flask
├── model.py               # Training model ML
├── requirements.txt       # Dependencies
├── README.md              # Dokumentasi
├── model.pkl              # Model terlatih
├── data/
│   └── villages.csv       # Data desa Riau
├── static/
│   └── js/
│       └── script.js      # JavaScript frontend
└── templates/
    └── index.html         # Template HTML
```

## Instalasi dan Jalankan Lokal

1. Clone atau download proyek ini ke folder `E:\KERJA PRAKTIK\Website Projek Kp`

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Jalankan training model (opsional, model.pkl sudah tersedia):
   ```
   python model.py
   ```

4. Jalankan aplikasi:
   ```
   python app.py
   ```

5. Buka browser ke `http://localhost:5000`

## Deployment ke Render (Gratis)

1. Buat akun di [Render](https://render.com)

2. Connect GitHub repository:
   - Push kode ke GitHub repo baru
   - Di Render, pilih "New Web Service"
   - Connect GitHub repo

3. Konfigurasi deployment:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python app.py`
   - Environment Variables: Jika perlu (misal untuk GEE API key)

4. Deploy dan dapatkan URL publik

## Penggunaan

1. Pilih tanggal di form
2. Klik "Prediksi"
3. Lihat hasil di peta dan daftar desa
4. Periksa panel notifikasi untuk instruksi

## Teknologi

- Backend: Flask, scikit-learn, XGBoost, pandas, numpy
- Frontend: HTML, Tailwind CSS, Leaflet JS
- ML: Stacking Classifier dengan 100% Recall target

## Catatan

- Data desa menggunakan simulasi untuk demo
- Model dilatih dengan data sintetis
- Untuk data real GEE, perlu autentikasi API
