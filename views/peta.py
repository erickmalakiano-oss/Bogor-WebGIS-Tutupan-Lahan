import folium
import streamlit as st
from folium.plugins import Fullscreen, MiniMap, MeasureControl, LocateControl
from streamlit_folium import st_folium

from utils.data_loader import load_boundary, RASTER_2020, RASTER_2021, RASTER_CHANGE, file_info
from utils.raster_utils import raster_overlay_landcover, raster_overlay_change
from utils.style import section_header, callout, page_header, get_theme, CLASS_COLORS, CLASS_ICONS


def _legend_html(theme):
    rows = ""
    for kelas, color in CLASS_COLORS.items():
        rows += (
            f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px;">'
            f'<span style="width:14px;height:14px;border-radius:3px;background:{color};'
            f'display:inline-block;border:1px solid rgba(0,0,0,0.25);"></span>'
            f'<span style="font-size:12px;color:{theme["ink"]};">{kelas}</span></div>'
        )
    return f"""
    <div style="
        position: fixed; bottom: 24px; left: 24px; z-index: 9999;
        background: {theme['surface']}; padding: 10px 14px; border-radius: 10px;
        box-shadow: {theme['shadow']}; font-family: sans-serif;
        border: 1px solid {theme['border']};">
        <div style="font-weight:700; font-size:12.5px; margin-bottom:6px; color:{theme['ink']};">Legenda Penutupan Lahan</div>
        {rows}
    </div>
    """


def render():
    theme = get_theme()
    page_header(
        eyebrow="Peta",
        title="Peta Interaktif Penutupan Lahan Kota Bogor",
        sub=(
            "Gunakan panel kontrol di bawah untuk memilih peta dasar dan layer "
            "raster penutupan lahan. Klik area kecamatan untuk melihat detail."
        ),
        icon_name="map",
    )
    callout(
        "Gunakan <b>Layer Control</b> di pojok kanan atas peta untuk mengatur "
        "tampilan layer yang ditampilkan."
    )

    try:
        gdf = load_boundary()
    except Exception as e:
        st.error(f"Gagal memuat data batas administrasi: {e}")
        return

    center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]

    # ---------- Panel kontrol ----------
    col_a, col_b, col_c = st.columns([1.3, 1.3, 1])
    with col_a:
        basemap = st.selectbox(
            "Peta Dasar",
            ["OpenStreetMap", "CartoDB Positron (Light)", "CartoDB Dark Matter", "Citra Satelit (Esri)"],
        )
    with col_b:
        layer_raster = st.selectbox(
            "Layer Penutupan Lahan",
            ["Tidak ada", "Penutupan Lahan 2020", "Penutupan Lahan 2021", "Deteksi Perubahan 2020–2021"],
        )
    with col_c:
        opacity = st.slider("Opasitas Layer", 0.1, 1.0, 0.75, 0.05)

    zoom_level = st.slider("Level Zoom Awal", 10, 16, 12, 1)

    # ---------- Basemap ----------
    tiles_map = {
        "OpenStreetMap": "OpenStreetMap",
        "CartoDB Positron (Light)": "CartoDB Positron",
        "CartoDB Dark Matter": "CartoDB Dark_Matter",
    }

    if basemap == "Citra Satelit (Esri)":
        m = folium.Map(
            location=center, zoom_start=zoom_level, control_scale=True,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri, Maxar, Earthstar Geographics",
        )
    else:
        m = folium.Map(location=center, zoom_start=zoom_level, control_scale=True, tiles=tiles_map[basemap])

    # Layer dasar tambahan agar bisa dipilih via LayerControl
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap", show=False).add_to(m)
    folium.TileLayer("CartoDB Positron", name="CartoDB Positron", show=False).add_to(m)
    folium.TileLayer("CartoDB Dark_Matter", name="CartoDB Dark Matter", show=False).add_to(m)
    folium.TileLayer(
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        name="Citra Satelit (Esri)", attr="Esri, Maxar, Earthstar Geographics", show=False,
    ).add_to(m)

    # ---------- Layer raster (penutupan lahan / perubahan) ----------
    raster_info_text = None
    if layer_raster == "Penutupan Lahan 2020":
        ada, ukuran = file_info(RASTER_2020)
        if ada:
            data_url, bounds, _ = raster_overlay_landcover(RASTER_2020)
            folium.raster_layers.ImageOverlay(
                image=data_url, bounds=bounds, opacity=opacity, name="Penutupan Lahan 2020"
            ).add_to(m)
            raster_info_text = f"Raster 2020 dimuat ({ukuran:.2f} MB)."
        else:
            st.warning("File raster 2020 tidak ditemukan.")
    elif layer_raster == "Penutupan Lahan 2021":
        ada, ukuran = file_info(RASTER_2021)
        if ada:
            data_url, bounds, _ = raster_overlay_landcover(RASTER_2021)
            folium.raster_layers.ImageOverlay(
                image=data_url, bounds=bounds, opacity=opacity, name="Penutupan Lahan 2021"
            ).add_to(m)
            raster_info_text = f"Raster 2021 dimuat ({ukuran:.2f} MB)."
        else:
            st.warning("File raster 2021 tidak ditemukan.")
    elif layer_raster == "Deteksi Perubahan 2020–2021":
        ada, ukuran = file_info(RASTER_CHANGE)
        if ada:
            data_url, bounds, pct = raster_overlay_change(RASTER_CHANGE)
            folium.raster_layers.ImageOverlay(
                image=data_url, bounds=bounds, opacity=opacity, name="Deteksi Perubahan 2020–2021"
            ).add_to(m)
            raster_info_text = f"± {pct:.1f}% area terdeteksi berubah antara 2020–2021."
        else:
            st.warning("File raster deteksi perubahan tidak ditemukan.")

    # ---------- Layer batas administrasi ----------
    folium.GeoJson(
        gdf,
        name="Batas Kecamatan",
        tooltip=folium.GeoJsonTooltip(fields=["kecamatan"], aliases=["Kecamatan:"], sticky=True),
        popup=folium.GeoJsonPopup(fields=["kecamatan", "luas_ha"], aliases=["Kecamatan:", "Luas (ha):"]),
        style_function=lambda f: {"fillColor": "#2e7d32", "color": "#1b5e20", "weight": 2.5, "fillOpacity": 0.05},
        highlight_function=lambda f: {"weight": 4, "color": "#f9a825", "fillOpacity": 0.15},
    ).add_to(m)

    # ---------- Plugin profesional ----------
    Fullscreen(position="topleft").add_to(m)
    MiniMap(toggle_display=True, position="bottomright").add_to(m)
    MeasureControl(primary_length_unit="meters", primary_area_unit="hectares").add_to(m)
    LocateControl().add_to(m)
    folium.LayerControl(collapsed=False).add_to(m)
    m.get_root().html.add_child(folium.Element(_legend_html(theme)))

    st_folium(m, width=None, height=580, returned_objects=[])

    if raster_info_text:
        st.caption(raster_info_text)

    st.caption(
        "Gunakan scroll untuk zoom, drag untuk menggeser peta, tombol fullscreen "
        "(pojok kiri atas) untuk tampilan penuh, dan penggaris untuk mengukur jarak/luas."
    )

    # ---------- Info wilayah ----------
    section_header("straighten", "Detail Wilayah Kecamatan")
    tabel = gdf[["kecamatan", "luas_ha"]].sort_values("luas_ha", ascending=False).reset_index(drop=True)
    tabel.index += 1
    tabel = tabel.rename(columns={"kecamatan": "Kecamatan", "luas_ha": "Luas (ha)"})
    st.dataframe(
        tabel.style.format({"Luas (ha)": "{:,.2f}"}).background_gradient(cmap="Greens", subset=["Luas (ha)"]),
        use_container_width=True,
        height=260,
    )
