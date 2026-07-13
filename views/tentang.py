import streamlit as st

from utils.data_loader import load_boundary
from utils.style import section_header, callout, page_header, icon, get_theme


def render():
    theme = get_theme()
    page_header(
        eyebrow="Tentang",
        title="Tentang Aplikasi",
        sub="Metodologi, sumber data, dan cakupan wilayah studi WebGIS ini.",
        icon_name="info",
    )

    col1, col2 = st.columns([2, 1], gap="large")
    with col1:
        st.markdown(
            """
            #### WebGIS Penutupan Lahan Kota Bogor

            Aplikasi **WebGIS interaktif** ini menyajikan hasil analisis perubahan
            **penutupan lahan** di Kota Bogor menggunakan citra satelit **Sentinel-2**
            dan algoritma klasifikasi **Random Forest**, dibandingkan antara tahun
            **2020** dan **2021**.

            Dibangun dengan teknologi open-source untuk mendukung transparansi,
            reproduksibilitas, dan kemudahan akses terhadap data spasial perubahan
            lingkungan di wilayah perkotaan Kota Bogor.
            """
        )
        callout(
            "<b>Tujuan:</b> Memetakan dan memantau dinamika penutupan lahan "
            "sebagai bahan evaluasi tata ruang dan pengambilan keputusan berbasis data."
        )
    with col2:
        st.markdown(
            f"""
            <div class="plain-card">
                {icon('location_city', 30)}
                <div class="pc-title">Kota Bogor</div>
                <div class="pc-sub">Provinsi Jawa Barat</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tab1, tab2, tab3 = st.tabs(["Wilayah Studi", "Data & Metode", "Referensi"])

    with tab1:
        st.markdown("##### Cakupan Wilayah")
        try:
            gdf = load_boundary()
            kec_list = gdf["kecamatan"].tolist()
        except Exception:
            kec_list = ["Bogor Barat", "Bogor Selatan", "Bogor Tengah", "Bogor Timur", "Bogor Utara", "Tanah Sereal"]

        col_a, col_b = st.columns([1, 1])
        with col_a:
            st.markdown(
                """
                | Parameter | Nilai |
                |---|---|
                | **Kota** | Bogor |
                | **Provinsi** | Jawa Barat |
                | **Jumlah Kecamatan** | 6 |
                | **Sistem Proyeksi** | EPSG:4326 (WGS 84) |
                """
            )
        with col_b:
            st.markdown("**Daftar Kecamatan:**")
            cols = st.columns(2)
            for i, kec in enumerate(kec_list):
                cols[i % 2].markdown(f"- {kec}")

    with tab2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(
                """
                **Citra Satelit**
                - Sensor: Sentinel-2 (MSI)
                - Resolusi spasial: 10 m (multispektral)
                - Tahun akuisisi: 2020 dan 2021
                - Sumber: Copernicus Open Access Hub / USGS Earth Explorer
                """
            )
        with c2:
            st.markdown(
                """
                **Data Pendukung**
                - Batas administrasi kecamatan Kota Bogor
                - Format data: Shapefile, GeoTIFF, CSV
                - Sistem proyeksi: EPSG:4326 (WGS 84)
                """
            )
        st.divider()
        st.markdown("##### Alur Metodologi")
        m1, m2, m3 = st.columns(3)
        with m1:
            with st.container(border=True):
                st.markdown("**① Pra-pemrosesan**")
                st.markdown("- Koreksi atmosfer\n- Cropping & masking\n- Komposit citra")
        with m2:
            with st.container(border=True):
                st.markdown("**② Klasifikasi**")
                st.markdown("- Algoritma: Random Forest\n- Fitur: Band spektral + indeks\n- 5 kelas penutupan lahan")
        with m3:
            with st.container(border=True):
                st.markdown("**③ Validasi & Analisis**")
                st.markdown("- Confusion matrix\n- Post-classification change detection\n- Visualisasi WebGIS")

        with st.expander("Kelas Penutupan Lahan", icon=":material/forest:", expanded=True):
            kelas = [
                ("forest", "Vegetasi", "Hutan kota, ruang terbuka hijau, dan area vegetasi rapat"),
                ("water_drop", "Badan Air", "Sungai, situ/kolam, dan saluran air"),
                ("terrain", "Lahan Terbuka", "Tanah kosong dan area terbuka non-vegetasi"),
                ("location_city", "Lahan Terbangun", "Permukiman, jalan, dan bangunan komersial"),
                ("agriculture", "Pertanian", "Sawah, ladang, dan area budidaya pertanian"),
            ]
            for icon_name, nama, desk in kelas:
                st.markdown(f"{icon(icon_name, 16)} &nbsp;**{nama}** — {desk}", unsafe_allow_html=True)

    with tab3:
        st.markdown(
            """
            ##### Referensi

            1. Congalton, R. G., & Green, K. (2019). *Assessing the Accuracy of
               Remotely Sensed Data: Principles and Practices*. CRC Press.
            2. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5–32.
            3. European Space Agency. (2015). *Sentinel-2 User Handbook*.
            4. Peraturan Daerah Kota Bogor tentang Rencana Tata Ruang Wilayah Kota Bogor.
            """
        )
        st.divider()
        st.markdown(
            f"""
            <div style="text-align:center;color:{theme['muted']};font-size:0.85rem;">
                Dikembangkan sebagai bagian dari studi analisis spasial perubahan
                penutupan lahan — Universitas Ibn Khaldun, Bogor.
            </div>
            """,
            unsafe_allow_html=True,
        )
