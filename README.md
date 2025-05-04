# Aplikasi Analisis Sentimen Komentar Instagram

Aplikasi web untuk menganalisis sentimen komentar Instagram menggunakan Flask dan Python.

## Fitur

- 📊 Dashboard visualisasi data
- 🔍 Analisis sentimen komentar baru
- 📈 Grafik interaktif menggunakan Plotly
- 🎨 Antarmuka pengguna yang modern dan responsif

## Persyaratan Sistem

- Python 3.7 atau lebih baru
- pip (package manager Python)

## Instalasi

1. Clone repositori ini:
```bash
git clone [URL_REPOSITORI]
cd [NAMA_FOLDER]
```

2. Buat dan aktifkan virtual environment (opsional tapi direkomendasikan):
```bash
python -m venv venv
source venv/bin/activate  # Untuk Linux/Mac
venv\Scripts\activate     # Untuk Windows
```

3. Install dependensi:
```bash
pip install -r requirements.txt
```

## Penggunaan

1. Jalankan aplikasi:
```bash
python app.py
```

2. Buka browser dan akses:
```
http://localhost:5000
```

## Struktur Proyek

```
.
├── app.py              # File utama aplikasi Flask
├── requirements.txt    # Daftar dependensi
├── templates/          # Folder template HTML
│   └── index.html     # Template halaman utama
└── komentar_dengan_sentimen.csv  # Dataset komentar
```

## API Endpoints

- `GET /`: Halaman utama aplikasi
- `GET /api/visualizations`: Mendapatkan data visualisasi
- `POST /api/analyze`: Menganalisis sentimen komentar baru

## Lisensi

MIT 