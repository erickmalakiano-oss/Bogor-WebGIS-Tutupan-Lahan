"""
Modul pemuatan data terpusat untuk WebGIS Penutupan Lahan Kota Bogor.
Semua path dan pembacaan data dikonsolidasikan di sini agar konsisten
dan mudah dipelihara (sesuai isi folder data/ yang sebenarnya).
"""

import os
import pandas as pd
import geopandas as gpd
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

BOUNDARY_SHP = os.path.join(DATA_DIR, "boundary", "kecamatan_kota_bogor.shp")

CSV_LUAS = os.path.join(DATA_DIR, "csv", "StatistikLuas_2020_2021_Final.csv")
CSV_CHANGE_MATRIX = os.path.join(DATA_DIR, "csv", "ChangeMatrix_2020_2021.csv")
CSV_CLASSIFICATION_REPORT = os.path.join(DATA_DIR, "csv", "classification_report.csv")
CSV_CONFUSION_MATRIX = os.path.join(DATA_DIR, "csv", "confusion_matrix.csv")
CSV_FEATURE_IMPORTANCE = os.path.join(DATA_DIR, "csv", "feature_importance.csv")

RASTER_2020 = os.path.join(DATA_DIR, "raster", "landcover_2020_final.tif")
RASTER_2021 = os.path.join(DATA_DIR, "raster", "landcover_2021_final.tif")
RASTER_CHANGE = os.path.join(DATA_DIR, "raster", "ChangeDetection_2020_2021.tif")

# Urutan kelas baku (1..5) sesuai skema klasifikasi Random Forest yang digunakan.
# PENTING: sesuaikan urutan ini apabila encoding nilai piksel pada raster
# hasil klasifikasi berbeda dari urutan berikut.
CLASS_ORDER = ["Vegetasi", "Badan Air", "Lahan Terbuka", "Lahan Terbangun", "Pertanian"]


@st.cache_data(show_spinner=False)
def load_boundary():
    """Baca batas administrasi kecamatan Kota Bogor (shapefile)."""
    gdf = gpd.read_file(BOUNDARY_SHP)
    if gdf.crs is None:
        gdf = gdf.set_crs("EPSG:4326")
    gdf = gdf.to_crs("EPSG:4326")

    # Hitung luas akurat memakai proyeksi UTM zona Bogor (48S)
    gdf_proj = gdf.to_crs("EPSG:32748")
    gdf = gdf.copy()
    gdf["luas_ha"] = gdf_proj.geometry.area / 10000.0

    # Samakan nama kolom kecamatan
    name_col = "NAME_3" if "NAME_3" in gdf.columns else gdf.columns[0]
    gdf = gdf.rename(columns={name_col: "kecamatan"})
    return gdf


@st.cache_data(show_spinner=False)
def load_luas_stats():
    """Baca statistik luas penutupan lahan 2020 vs 2021 per kelas."""
    df = pd.read_csv(CSV_LUAS)
    df = df.rename(columns={
        "Kelas": "Kelas",
        "2020 (ha)": "2020",
        "2021 (ha)": "2021",
        "Perubahan (ha)": "Perubahan",
    })
    df = df.set_index("Kelas")
    # urutkan sesuai CLASS_ORDER bila cocok
    ordered = [c for c in CLASS_ORDER if c in df.index]
    sisanya = [c for c in df.index if c not in ordered]
    df = df.loc[ordered + sisanya]
    return df


@st.cache_data(show_spinner=False)
def load_change_matrix():
    """Baca matriks transisi/perubahan antar kelas 2020->2021."""
    df = pd.read_csv(CSV_CHANGE_MATRIX, index_col=0)
    return df


@st.cache_data(show_spinner=False)
def load_classification_report():
    df = pd.read_csv(CSV_CLASSIFICATION_REPORT, index_col=0)
    return df


@st.cache_data(show_spinner=False)
def load_confusion_matrix():
    df = pd.read_csv(CSV_CONFUSION_MATRIX)
    return df


@st.cache_data(show_spinner=False)
def load_feature_importance():
    df = pd.read_csv(CSV_FEATURE_IMPORTANCE)
    df = df.sort_values("importance", ascending=False)
    return df


def file_info(path):
    """Kembalikan (ada/tidak, ukuran MB) untuk sebuah file."""
    if os.path.exists(path):
        return True, os.path.getsize(path) / (1024 * 1024)
    return False, 0.0
