import streamlit as st

from utils.style import inject_global_css, app_footer, theme_toggle_button, icon
from views import beranda, peta, statistik, visualisasi, tentang

st.set_page_config(
    page_title="WebGIS Penutupan Lahan Kota Bogor",
    page_icon=":material/travel_explore:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# State tema (terang/gelap) & navigasi
# =========================================================
if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

if "active_page" not in st.session_state:
    st.session_state["active_page"] = "beranda"

inject_global_css()

PAGES = {
    "beranda": {"label": "Beranda", "icon": ":material/home:", "render": beranda.render},
    "peta": {"label": "Peta Interaktif", "icon": ":material/map:", "render": peta.render},
    "statistik": {"label": "Statistik", "icon": ":material/bar_chart:", "render": statistik.render},
    "visualisasi": {"label": "Visualisasi & Evaluasi", "icon": ":material/insights:", "render": visualisasi.render},
    "tentang": {"label": "Tentang", "icon": ":material/info:", "render": tentang.render},
}

# =========================================================
# Sidebar — branding & navigasi kustom
# =========================================================
with st.sidebar:
    st.markdown(
        f"""
        <div class="sidebar-brand">
            <div class="logo-box">{icon('travel_explore', 22)}</div>
            <div class="brand-text">
                <b>WebGIS Bogor</b>
                <span>Penutupan Lahan 2020&ndash;2021</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for key, meta in PAGES.items():
        is_active = st.session_state["active_page"] == key
        label = meta["label"] + ("  ●" if is_active else "")
        if st.button(label, key=f"nav_{key}", icon=meta["icon"], use_container_width=True):
            st.session_state["active_page"] = key
            st.rerun()

    st.write("")
    theme_toggle_button()

    st.markdown(
        f"""
        <div class="sidebar-foot">
            {icon('satellite_alt', 15)} Sumber citra: Sentinel-2 (MSI)<br>
            {icon('smart_toy', 15)} Model: Random Forest Classifier<br>
            {icon('location_on', 15)} Wilayah: Kota Bogor, Jawa Barat
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# Render halaman aktif
# =========================================================
current = PAGES[st.session_state["active_page"]]
current["render"]()

app_footer()
