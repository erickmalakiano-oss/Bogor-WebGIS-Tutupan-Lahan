# WebGIS Penutupan Lahan Kota Bogor — Versi Diperbarui

Paket ini berisi **kode aplikasi yang sudah dirombak** (bukan folder `data/`,
karena ukurannya besar dan tidak berubah). Ikuti langkah berikut untuk
memasangnya ke proyek `BogorWebGIS` Anda.

## 1. Apa yang berubah

- ❌ **Menu multipage bawaan Streamlit dihapus** (folder `pages/` lama tidak
  dipakai lagi). Aplikasi sekarang **langsung membuka halaman Beranda**,
  dengan navigasi kustom di sidebar (tombol Beranda, Peta, Statistik,
  Visualisasi, Tentang) — tampil lebih profesional dan bisa dikembangkan.
- 🎨 **Desain baru**: hero banner, kartu KPI, kartu fitur, warna & tipografi
  konsisten (Poppins + Inter), legenda peta, palet warna kelas seragam di
  semua halaman.
- 🗺️ **Fitur WebGIS profesional** pada halaman Peta:
  - Pilihan basemap (OSM, CartoDB Light/Dark, Citra Satelit Esri)
  - Overlay raster penutupan lahan **2018**, **2024**, dan **peta perubahan**
    langsung di atas peta, dengan slider opasitas
  - Fullscreen, MiniMap, Measure Tool (ukur jarak/luas), Locate Me, Layer
    Control, dan legenda kelas
  - Tabel luas per kecamatan
- 📊 **Statistik & Visualisasi diperbaiki** agar sesuai data asli Anda:
  `StatistikLuas_2018_2024_Final.csv`, `ChangeMatrix_2018_2024.csv`,
  `classification_report.csv`, `confusion_matrix.csv`,
  `feature_importance.csv` — sebelumnya kode lama merujuk file CSV yang
  **tidak ada** (`landcover_area.csv`, `change_detection.csv`) dan skema
  3 tahun (2018/2021/2024), padahal data Anda sebenarnya 2 tahun (2018/2024)
  dengan 5 kelas: Vegetasi, Badan Air, Lahan Terbuka, Lahan Terbangun,
  Pertanian. Bagian evaluasi model (akurasi, confusion matrix, feature
  importance) sekarang ditampilkan — sebelumnya tidak pernah dipakai sama
  sekali di WebGIS.
- 🧩 Kode dipecah rapi: `app.py` (entry point + navigasi), `views/`
  (isi tiap halaman), `utils/` (data loader, styling, raster overlay).

## 2. Cara memasang

1. Ekstrak isi ZIP ini.
2. Salin/replace ke dalam folder proyek `BogorWebGIS` Anda:
   - `app.py` → timpa file lama
   - folder `views/` → tambahkan (baru)
   - folder `utils/` → tambahkan (baru)
   - `requirements.txt` → timpa/gabungkan
   - `.streamlit/config.toml` → tambahkan (opsional, untuk tema warna)
3. **Hapus folder `pages/` lama** (`1_WebGIS.py`, `2_Statistik.py`,
   `3_Visualisasi.py`, `4_Tentang.py`) — sudah digantikan oleh `views/` +
   navigasi kustom di `app.py`. Kalau folder `pages/` masih ada, Streamlit
   akan tetap menampilkan menu multipage bawaan di sidebar.
4. Folder `data/`, `assets/`, `.claude/` **tidak perlu diubah** — biarkan
   seperti semula.
5. Install dependensi (jika belum lengkap):
   ```bash
   pip install -r requirements.txt
   ```
6. Jalankan:
   ```bash
   streamlit run app.py
   ```

## 3. Catatan penting — pemetaan kelas raster

Di `utils/raster_utils.py`, nilai piksel raster `landcover_2018_final.tif`
dan `landcover_2024_final.tif` diasumsikan bernilai **1–5** sesuai urutan:

```
1 = Vegetasi
2 = Badan Air
3 = Lahan Terbuka
4 = Lahan Terbangun
5 = Pertanian
```

Jika urutan/encoding kelas pada hasil klasifikasi Anda **berbeda**, silakan
sesuaikan urutan `CLASS_ORDER` di `utils/data_loader.py` (baris ±25) agar
warna overlay peta sesuai dengan kelas yang sebenarnya.

## 4. Struktur folder akhir

```
BogorWebGIS/
├── app.py
├── requirements.txt
├── .streamlit/
│   └── config.toml
├── views/
│   ├── beranda.py
│   ├── peta.py
│   ├── statistik.py
│   ├── visualisasi.py
│   └── tentang.py
├── utils/
│   ├── data_loader.py
│   ├── raster_utils.py
│   └── style.py
├── data/            (tidak diubah)
└── assets/          (tidak diubah)
```
