import streamlit as st

from utils.data_loader import load_boundary, load_luas_stats, load_classification_report
from utils.style import section_header, kpi_card, page_header, icon, CLASS_COLORS, CLASS_ICONS


def _go(page_key):
    st.session_state["active_page"] = page_key
    st.rerun()


def render():
    # ---------- Header halaman ----------
    page_header(
        eyebrow="WebGIS · Pemetaan Perubahan Lahan",
        title="Pemantauan Penutupan Lahan Kota Bogor 2020 — 2021",
        sub=(
            "Platform WebGIS interaktif untuk memvisualisasikan hasil klasifikasi "
            "penutupan lahan berbasis citra satelit Sentinel-2 dan algoritma "
            "Random Forest, mencakup enam kecamatan di Kota Bogor."
        ),
        icon_name="travel_explore",
    )

    col_btn1, col_btn2, _ = st.columns([1, 1, 3])
    with col_btn1:
        if st.button("Buka Peta Interaktif", icon=":material/map:", use_container_width=True, type="primary"):
            _go("peta")
    with col_btn2:
        if st.button("Lihat Statistik", icon=":material/bar_chart:", use_container_width=True):
            _go("statistik")

    st.write("")

    # ---------- KPI ----------
    try:
        gdf = load_boundary()
        luas_total = gdf["luas_ha"].sum()
        jumlah_kec = len(gdf)
    except Exception:
        luas_total, jumlah_kec = None, None

    try:
        luas_df = load_luas_stats()
        total_2021 = luas_df["2021"].sum()
        total_2020 = luas_df["2020"].sum()
        delta_pct = (total_2021 - total_2020) / total_2020 * 100
    except Exception:
        total_2021, delta_pct = None, None

    try:
        report_df = load_classification_report()
        akurasi = report_df.loc["accuracy"].iloc[0] * 100
    except Exception:
        akurasi = None

    section_header("location_on", "Ringkasan Wilayah Kajian")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Jumlah Kecamatan", f"{jumlah_kec}" if jumlah_kec else "—", "Kota Bogor", icon_name="apartment")
    with c2:
        kpi_card(
            "Total Luas Wilayah",
            f"{luas_total:,.0f} ha" if luas_total else "—",
            f"± {luas_total/100:,.1f} km²" if luas_total else None,
            delta_up=True,
            icon_name="crop_square",
        )
    with c3:
        kpi_card(
            "Total Tutupan Terklasifikasi (2021)",
            f"{total_2021:,.0f} ha" if total_2021 else "—",
            (f"{delta_pct:+.2f}% sejak 2020" if delta_pct is not None else None),
            delta_up=(delta_pct is not None and delta_pct >= 0),
            icon_name="layers",
        )
    with c4:
        kpi_card(
            "Akurasi Model Random Forest",
            f"{akurasi:.1f}%" if akurasi else "—",
            "Classification Report",
            icon_name="track_changes",
        )

    st.write("")

    # ---------- Feature cards / navigation ----------
    section_header("explore", "Jelajahi Aplikasi")
    fc1, fc2, fc3, fc4 = st.columns(4)

    features = [
        ("map", "Peta Interaktif", "Visualisasi spasial batas kecamatan dan overlay raster penutupan lahan 2020 & 2021.", "peta"),
        ("bar_chart", "Statistik Luasan", "Tabel dan grafik luas tiap kelas penutupan lahan per tahun beserta perubahannya.", "statistik"),
        ("insights", "Visualisasi & Evaluasi", "Matriks perubahan, evaluasi akurasi model, dan tingkat kepentingan fitur.", "visualisasi"),
        ("info", "Tentang Aplikasi", "Metodologi, sumber data, dan cakupan wilayah studi.", "tentang"),
    ]

    for col, (icon_name, title, desc, key) in zip([fc1, fc2, fc3, fc4], features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon(icon_name, 22)}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Buka", icon=":material/arrow_forward:", key=f"home_nav_{key}", use_container_width=True):
                _go(key)

    st.write("")

    # ---------- Legend preview ----------
    section_header("palette", "Kelas Penutupan Lahan")
    legend_cols = st.columns(5)
    for col, kelas in zip(legend_cols, CLASS_COLORS.keys()):
        with col:
            color = CLASS_COLORS[kelas]
            icon_name = CLASS_ICONS.get(kelas, "circle")
            st.markdown(
                f"""
                <div class="legend-card">
                    <div class="legend-icon" style="background:{color};">{icon(icon_name, 18)}</div>
                    <div class="legend-label">{kelas}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
