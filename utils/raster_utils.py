"""
Modul utilitas raster: mengubah GeoTIFF hasil klasifikasi penutupan lahan
menjadi overlay gambar (PNG base64) yang dapat ditampilkan di peta Folium,
lengkap dengan bounding box dalam WGS84.
"""

import base64
import io

import numpy as np
import rasterio
from rasterio.warp import transform_bounds
import streamlit as st
from PIL import Image

from utils.style import CLASS_COLORS
from utils.data_loader import CLASS_ORDER

# Warna kelas berdasarkan nilai piksel 1..5, mengikuti CLASS_ORDER.
# Sesuaikan pemetaan ini jika encoding nilai piksel raster berbeda.
PIXEL_CLASS_MAP = {i + 1: kelas for i, kelas in enumerate(CLASS_ORDER)}

# Palet untuk peta perubahan (change detection): biasanya biner/berkode
# 0 = tidak berubah, 1 = berubah (atau kode arah perubahan tertentu).
CHANGE_COLOR_NO_CHANGE = (158, 158, 158, 90)   # abu-abu transparan tipis
CHANGE_COLOR_CHANGED = (198, 40, 40, 200)      # merah tegas


@st.cache_data(show_spinner=False)
def raster_overlay_landcover(path: str):
    """
    Baca raster klasifikasi penutupan lahan (single-band, nilai 1-5)
    dan kembalikan (data_url_png, bounds_wgs84, unique_values).
    """
    with rasterio.open(path) as src:
        band = src.read(1)
        nodata = src.nodata
        bounds = src.bounds
        src_crs = src.crs

        bounds_wgs84 = transform_bounds(src_crs, "EPSG:4326", *bounds)

        h, w = band.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)

        for val, kelas in PIXEL_CLASS_MAP.items():
            hex_color = CLASS_COLORS.get(kelas, "#999999")
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            mask = band == val
            rgba[mask] = (r, g, b, 210)

        # transparan untuk nodata / nilai 0 / di luar kelas
        if nodata is not None:
            rgba[band == nodata] = (0, 0, 0, 0)
        rgba[band == 0] = (0, 0, 0, 0)

        img = Image.fromarray(rgba, mode="RGBA")
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        data_url = f"data:image/png;base64,{b64}"

        south, west, north, east = (
            bounds_wgs84[1], bounds_wgs84[0], bounds_wgs84[3], bounds_wgs84[2]
        )
        folium_bounds = [[south, west], [north, east]]

        unique_vals = sorted(set(np.unique(band)) - {0, nodata if nodata is not None else -9999})

    return data_url, folium_bounds, unique_vals


@st.cache_data(show_spinner=False)
def raster_overlay_change(path: str):
    """
    Baca raster deteksi perubahan (change detection) dan kembalikan overlay
    PNG (0 = tidak berubah/abu transparan, selain 0 = berubah/merah).
    """
    with rasterio.open(path) as src:
        band = src.read(1)
        nodata = src.nodata
        bounds = src.bounds
        src_crs = src.crs

        bounds_wgs84 = transform_bounds(src_crs, "EPSG:4326", *bounds)

        h, w = band.shape
        rgba = np.zeros((h, w, 4), dtype=np.uint8)

        no_change_mask = band == 0
        rgba[no_change_mask] = CHANGE_COLOR_NO_CHANGE
        rgba[~no_change_mask] = CHANGE_COLOR_CHANGED

        if nodata is not None:
            rgba[band == nodata] = (0, 0, 0, 0)

        img = Image.fromarray(rgba, mode="RGBA")
        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        b64 = base64.b64encode(buf.getvalue()).decode()
        data_url = f"data:image/png;base64,{b64}"

        south, west, north, east = (
            bounds_wgs84[1], bounds_wgs84[0], bounds_wgs84[3], bounds_wgs84[2]
        )
        folium_bounds = [[south, west], [north, east]]

        pct_berubah = float((~no_change_mask).sum()) / float(band.size) * 100

    return data_url, folium_bounds, pct_berubah
