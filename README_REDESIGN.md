# Paket Redesign — WebGIS Penutupan Lahan Kota Bogor

> **Update ke-2:** perbaikan lanjutan untuk bug sidebar. Penyebab
> sebenarnya adalah aturan `[data-testid="stToolbar"] {visibility:
> hidden;}` — di banyak versi Streamlit, tombol buka/tutup sidebar
> adalah bagian dari toolbar itu sendiri, jadi ikut tersembunyi.
> Sekarang toolbar tidak lagi disembunyikan (hanya tombol "Deploy" dan
> menu titik-tiga yang disembunyikan secara spesifik), sehingga tombol
> sidebar pasti tetap muncul & bisa diklik di versi Streamlit manapun.

> **Update ke-1:** paket ini sudah memuat perbaikan 2 bug yang dilaporkan:
> 1. Teks tidak terlihat di mode gelap (aturan warna teks sekarang
>    dipaksa `!important` supaya tidak ditimpa gaya bawaan Streamlit).
> 2. Sidebar tidak bisa dibuka lagi setelah ditutup sekali (sebelumnya
>    elemen `<header>` disembunyikan total, padahal tombol buka-tutup
>    sidebar ada di dalamnya — sekarang `<header>` dibuat transparan,
>    bukan disembunyikan, jadi tombolnya tetap berfungsi).


Paket ini **hanya berisi kode** (tidak ada folder `data/`), sesuai
struktur folder proyekmu yang sudah ada. Isinya: `app.py`, `utils/`,
`views/`, `requirements.txt`.

## Apa yang berubah dari versi sebelumnya

1. **Semua emoji dihapus**, diganti dengan **Google Material Symbols**
   (ikon garis modern, konsisten di seluruh halaman). Tidak perlu
   file aset gambar apa pun — cukup satu baris `<link>` Google Fonts
   yang sudah ditambahkan otomatis di `utils/style.py`.
2. **Desain baru "Minimalist Modern"**: latar terang/gelap netral,
   satu warna aksen (teal `#0f766e`), banyak whitespace, bayangan
   tipis, tanpa gradient hero banner yang berat. Font judul diganti
   ke Manrope (lebih modern & rapi untuk gaya minimalis).
3. **Mode terang/gelap**: tombol toggle baru di sidebar (di bawah
   menu navigasi). Klik untuk beralih, akan otomatis me-refresh
   tampilan.

## Cara test di folder lokalmu

1. Ekstrak paket ini.
2. Timpa (replace) `app.py`, folder `utils/`, dan folder `views/` di
   folder proyek lokalmu dengan yang ada di paket ini.
3. `requirements.txt` sudah mensyaratkan `streamlit>=1.32` (dibutuhkan
   untuk fitur ikon Material di tombol/tab). Kalau versi streamlit-mu
   lebih lama, jalankan:
   ```bash
   pip install -U "streamlit>=1.32"
   ```
4. Folder `data/`, `assets/`, `.claude/` **tidak perlu diubah** —
   biarkan seperti semula, kode ini otomatis memakai data yang sudah
   ada di sana.
5. Jalankan seperti biasa:
   ```bash
   streamlit run app.py
   ```

## Catatan jujur soal mode gelap

Toggle gelap/terang ini mengubah **semua elemen kustom** aplikasi:
latar halaman, sidebar, kartu KPI, kartu fitur, callout, tab, grafik
Plotly, dan legenda peta — semuanya otomatis menyesuaikan warna.

Tapi ada beberapa komponen **bawaan Streamlit** (bukan buatan kode
ini) yang kadang tidak 100% ikut berubah, tergantung versi Streamlit
yang kamu pakai — misalnya kotak tabel `st.dataframe`, dropdown
`selectbox`, dan slider. Ini keterbatasan dari sisi Streamlit sendiri
(tema bawaannya diatur terpisah dari CSS kustom aplikasi). Kalau saat
kamu test ternyata ada bagian yang terlihat kurang pas di mode gelap,
kabari saya — nanti saya sesuaikan lagi bagian spesifiknya.

## Setelah kamu cocok dan yakin

Salin `app.py`, `utils/`, `views/`, dan `requirements.txt` yang sudah
ditest ini ke folder ZIP siap-hosting yang sebelumnya sudah aku
berikan (folder yang sudah berisi data 2020/2021), menimpa file lama
di sana.
