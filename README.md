# Proyek Analisis Data: Bike Sharing Dataset 🚲

Analisis data penyewaan sepeda *Capital Bikeshare* (Washington D.C., 2011-2012) beserta dashboard interaktif berbasis Streamlit.

## Pertanyaan Bisnis
1. Pada jam berapa permintaan sepeda mencapai puncak di hari kerja dibandingkan akhir pekan/hari libur?
2. Seberapa besar penurunan penyewaan harian saat cuaca buruk, dan musim apa yang paling rendah?
3. Berapa pertumbuhan penyewaan 2012 dibanding 2011, dan apakah didorong pengguna registered atau casual?

Analisis lanjutan: *manual grouping* dan *binning* (waktu dalam sehari, kelompok suhu, tingkat permintaan harian, dan karakter pengguna).

## Struktur Direktori
```
submission
├───dashboard
│   ├───main_data.csv
│   └───dashboard.py
├───data
│   ├───day.csv
│   ├───hour.csv
│   └───Readme.txt
├───notebook.ipynb
├───README.md
├───requirements.txt
└───url.txt
```

## Setup Environment
```
conda create --name analyst python=3.10
conda activate analyst
pip install -r requirements.txt
```

## Menjalankan Dashboard
Dari folder utama proyek (`submission`), jalankan:
```
streamlit run dashboard/dashboard.py
```
Dashboard akan terbuka di `http://localhost:8501`.

## Menjalankan Notebook
Buka `notebook.ipynb` dari folder utama proyek (agar path `data/...` terbaca), lalu jalankan semua sel. Sel terakhir pada bagian Analisis Lanjutan akan menghasilkan `dashboard/main_data.csv`.

## Dashboard Online
Tautan Streamlit Cloud tersedia pada berkas `url.txt`.
