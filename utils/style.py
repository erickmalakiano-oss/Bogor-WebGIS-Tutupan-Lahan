"""
Modul styling terpusat untuk WebGIS Penutupan Lahan Kota Bogor.
Desain: Minimalist Modern - satu warna aksen, banyak whitespace,
bayangan tipis, mendukung mode terang & gelap.
Ikon menggunakan Google Material Symbols (bukan emoji).
"""

import streamlit as st

# ============================================================
# Palet warna kelas penutupan lahan (tetap sama di kedua tema,
# karena ini warna semantik data, bukan warna tema UI)
# ============================================================
CLASS_COLORS = {
    "Vegetasi": "#2e7d32",
    "Badan Air": "#1565c0",
    "Lahan Terbuka": "#a1887f",
    "Lahan Terbangun": "#c62828",
    "Pertanian": "#f9a825",
}

# Nama ikon Material Symbols (bukan emoji) untuk tiap kelas
CLASS_ICONS = {
    "Vegetasi": "forest",
    "Badan Air": "water_drop",
    "Lahan Terbuka": "terrain",
    "Lahan Terbangun": "location_city",
    "Pertanian": "agriculture",
}

# ============================================================
# Definisi tema terang & gelap
# ============================================================
THEMES = {
    "light": {
        "bg": "#fafafa",
        "surface": "#ffffff",
        "surface_alt": "#f4f4f5",
        "border": "#e4e4e7",
        "ink": "#18181b",
        "muted": "#71717a",
        "accent": "#0f766e",
        "accent_ink": "#ffffff",
        "accent_soft": "#e9f5f3",
        "success": "#15803d",
        "danger": "#b91c1c",
        "shadow": "0 1px 2px rgba(15,23,22,0.04), 0 4px 14px rgba(15,23,22,0.05)",
        "plotly_template": "plotly_white",
    },
    "dark": {
        "bg": "#131316",
        "surface": "#1c1c20",
        "surface_alt": "#202024",
        "border": "#2d2d33",
        "ink": "#f4f4f5",
        "muted": "#a1a1aa",
        "accent": "#2dd4bf",
        "accent_ink": "#0b1f1c",
        "accent_soft": "rgba(45,212,191,0.14)",
        "success": "#4ade80",
        "danger": "#f87171",
        "shadow": "0 1px 2px rgba(0,0,0,0.4), 0 4px 16px rgba(0,0,0,0.45)",
        "plotly_template": "plotly_dark",
    },
}


def get_theme_name() -> str:
    return st.session_state.get("theme", "light")


def get_theme() -> dict:
    return THEMES[get_theme_name()]


def toggle_theme():
    st.session_state["theme"] = "dark" if get_theme_name() == "light" else "light"


def icon(name: str, size: int = 20) -> str:
    """Kembalikan span Material Symbols inline untuk dipakai di dalam HTML kustom."""
    return f'<span class="material-symbols-outlined" style="font-size:{size}px;">{name}</span>'


def style_plot(fig):
    """Terapkan tema terang/gelap ke figure Plotly agar konsisten dengan UI."""
    t = get_theme()
    fig.update_layout(
        template=t["plotly_template"],
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color=t["ink"],
    )
    return fig


def inject_global_css():
    t = get_theme()
    st.markdown(
        f"""
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
        <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,300..500,0..1,-25..0" />
        <style>
            .material-symbols-outlined {{
                font-variation-settings: 'FILL' 0, 'wght' 400, 'GRAD' 0, 'opsz' 24;
                vertical-align: middle;
                line-height: 1;
            }}

            html, body, [class*="css"] {{
                font-family: 'Inter', sans-serif;
            }}
            h1, h2, h3, h4, .navbar-brand {{
                font-family: 'Manrope', sans-serif !important;
                font-weight: 700 !important;
            }}

            /* Sembunyikan elemen bawaan Streamlit yang tidak dipakai.
               PENTING: jangan sembunyikan <header> ATAU toolbar-nya —
               tombol untuk membuka/menutup sidebar ternyata adalah
               bagian dari elemen tersebut di banyak versi Streamlit.
               Kita hanya sembunyikan menu titik-tiga ("MainMenu") dan
               footer bawaan, sisanya dibiarkan aktif & terlihat. */
            #MainMenu {{visibility: hidden;}}
            footer {{visibility: hidden;}}
            [data-testid="stHeader"] {{
                background: transparent;
            }}
            [data-testid="stToolbar"] {{
                right: 1rem;
            }}
            /* Sembunyikan tombol "Deploy" saja (bukan seluruh toolbar) */
            [data-testid="stAppDeployButton"] {{display: none;}}
            [data-testid="stSidebarNav"] {{display: none;}}
            /* Nama data-testid tombol buka/tutup sidebar berbeda-beda
               antar versi Streamlit — kita pastikan semua kemungkinannya
               tetap terlihat & bisa diklik, dengan prioritas tertinggi. */
            [data-testid="stSidebarCollapsedControl"],
            [data-testid="stSidebarCollapseButton"],
            [data-testid="collapsedControl"],
            [data-testid="baseButton-headerNoPadding"] {{
                visibility: visible !important;
                display: flex !important;
                opacity: 1 !important;
                z-index: 999999 !important;
                color: {t['ink']} !important;
            }}
            [data-testid="stSidebarCollapsedControl"] svg,
            [data-testid="stSidebarCollapseButton"] svg,
            [data-testid="collapsedControl"] svg,
            [data-testid="stHeader"] svg {{
                fill: {t['ink']} !important;
            }}
            .block-container {{
                padding-top: 1.6rem;
                padding-bottom: 2rem;
                max-width: 1280px;
            }}

            :root {{
                --primary-color: {t['accent']};
                --background-color: {t['bg']};
                --secondary-background-color: {t['surface']};
                --text-color: {t['ink']};
            }}

            .stApp {{
                background: {t['bg']};
            }}

            /* Paksa warna teks di semua elemen konten agar tidak
               "tenggelam" oleh warna default Streamlit saat mode gelap */
            .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
            .stApp li, .stApp strong, .stApp em, .stApp small,
            .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6,
            [data-testid="stMarkdownContainer"],
            [data-testid="stMarkdownContainer"] *,
            [data-testid="stWidgetLabel"] p,
            [data-testid="stCaptionContainer"],
            [data-testid="stCaptionContainer"] *,
            [data-testid="stMetricLabel"],
            [data-testid="stMetricValue"],
            [data-testid="stMetricDelta"],
            [data-testid="stTable"], [data-testid="stTable"] * {{
                color: {t['ink']} !important;
            }}

            /* ===== Sidebar (flat minimalis) ===== */
            section[data-testid="stSidebar"] {{
                background: {t['surface']};
                border-right: 1px solid {t['border']};
            }}
            section[data-testid="stSidebar"] * {{
                color: {t['ink']} !important;
            }}
            section[data-testid="stSidebar"] .stButton>button {{
                width: 100%;
                text-align: left;
                background: transparent;
                border: 1px solid transparent;
                color: {t['ink']} !important;
                border-radius: 10px;
                padding: 0.5rem 0.8rem;
                margin-bottom: 0.2rem;
                font-weight: 500;
                font-size: 0.9rem;
                transition: all 0.12s ease-in-out;
                box-shadow: none;
            }}
            section[data-testid="stSidebar"] .stButton>button:hover {{
                background: {t['accent_soft']};
                border-color: {t['border']};
            }}
            section[data-testid="stSidebar"] .stButton>button:focus:not(:active) {{
                border-color: {t['accent']};
            }}
            .sidebar-brand {{
                display: flex;
                align-items: center;
                gap: 0.65rem;
                padding: 0.4rem 0 1.1rem 0;
                border-bottom: 1px solid {t['border']};
                margin-bottom: 1rem;
            }}
            .sidebar-brand .logo-box {{
                width: 38px; height: 38px;
                border-radius: 10px;
                background: {t['accent_soft']};
                color: {t['accent']};
                display: flex; align-items: center; justify-content: center;
            }}
            .sidebar-brand .brand-text b {{
                font-family: 'Manrope', sans-serif;
                font-size: 0.98rem;
                display:block;
                line-height: 1.15;
                color: {t['ink']};
            }}
            .sidebar-brand .brand-text span {{
                font-size: 0.7rem;
                color: {t['muted']};
            }}
            .sidebar-foot {{
                margin-top: 1.6rem;
                padding-top: 0.9rem;
                border-top: 1px solid {t['border']};
                font-size: 0.72rem;
                color: {t['muted']};
                line-height: 1.7;
            }}
            .sidebar-foot .material-symbols-outlined {{
                font-size: 15px; margin-right: 4px; color: {t['muted']};
            }}
            .theme-toggle-label {{
                font-size: 0.72rem;
                text-transform: uppercase;
                letter-spacing: 0.04em;
                color: {t['muted']};
                margin: 0.3rem 0 0.4rem 0;
                font-weight: 600;
            }}

            /* ===== Header halaman (pengganti hero banner gradient) ===== */
            .page-header {{
                border-bottom: 1px solid {t['border']};
                padding-bottom: 1.1rem;
                margin-bottom: 1.6rem;
            }}
            .page-eyebrow {{
                display: flex;
                align-items: center;
                gap: 0.4rem;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                font-size: 0.72rem;
                font-weight: 700;
                color: {t['accent']};
                margin-bottom: 0.5rem;
            }}
            .page-title {{
                font-family: 'Manrope', sans-serif;
                font-size: 1.9rem;
                font-weight: 800;
                margin: 0 0 0.5rem 0;
                line-height: 1.2;
                color: {t['ink']};
            }}
            .page-sub {{
                font-size: 0.95rem;
                max-width: 700px;
                color: {t['muted']};
                line-height: 1.6;
            }}

            /* ===== KPI cards ===== */
            .kpi-card {{
                background: {t['surface']};
                border: 1px solid {t['border']};
                border-radius: 14px;
                padding: 1.05rem 1.25rem;
                box-shadow: {t['shadow']};
                height: 100%;
            }}
            .kpi-label {{
                display: flex; align-items: center; gap: 0.35rem;
                font-size: 0.74rem;
                color: {t['muted']};
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.03em;
                margin-bottom: 0.4rem;
            }}
            .kpi-label .material-symbols-outlined {{ font-size: 16px; }}
            .kpi-value {{
                font-family: 'Manrope', sans-serif;
                font-size: 1.5rem;
                font-weight: 800;
                color: {t['ink']};
            }}
            /* Tombol primary (mis. "Buka Peta Interaktif") harus tetap
               berteks terang di atas latar warna aksen, jangan ikut
               dipaksa warna tinta gelap oleh reset umum di atas. */
            .stButton>button[kind="primary"],
            .stButton>button[kind="primary"] p,
            .stButton>button[kind="primary"] span,
            .stButton>button[kind="primary"] div {{
                color: {t['accent_ink']} !important;
            }}
            .stDownloadButton>button, .stDownloadButton>button * {{
                color: {t['ink']} !important;
            }}

            .kpi-delta-up {{ color: {t['success']}; font-weight: 600; font-size: 0.8rem; }}
            .kpi-delta-down {{ color: {t['danger']}; font-weight: 600; font-size: 0.8rem; }}

            /* ===== Feature / nav cards ===== */
            .feature-card {{
                background: {t['surface']};
                border: 1px solid {t['border']};
                border-radius: 14px;
                padding: 1.3rem 1.3rem 1rem 1.3rem;
                height: 100%;
                transition: all 0.15s ease-in-out;
                box-shadow: {t['shadow']};
            }}
            .feature-card:hover {{
                border-color: {t['accent']};
                transform: translateY(-2px);
            }}
            .feature-icon {{
                width: 44px; height: 44px;
                background: {t['accent_soft']};
                color: {t['accent']};
                border-radius: 10px;
                display: flex; align-items: center; justify-content: center;
                margin-bottom: 0.8rem;
            }}
            .feature-title {{
                font-family:'Manrope', sans-serif;
                font-weight: 700;
                font-size: 0.98rem;
                color: {t['ink']};
                margin-bottom: 0.3rem;
            }}
            .feature-desc {{
                font-size: 0.84rem;
                color: {t['muted']};
                line-height: 1.5;
            }}

            /* ===== Section headers ===== */
            .section-header {{
                display:flex;
                align-items:center;
                gap:0.55rem;
                margin: 0.2rem 0 1rem 0;
                color: {t['accent']};
            }}
            .section-header .material-symbols-outlined {{ font-size: 20px; }}
            .section-header h3 {{
                margin: 0;
                color: {t['ink']};
                font-size: 1.15rem;
            }}

            /* ===== Info callout ===== */
            .callout {{
                padding: 0.8rem 1.1rem;
                border-radius: 10px;
                border-left: 3px solid {t['accent']};
                background: {t['accent_soft']};
                margin-bottom: 1.2rem;
                font-size: 0.88rem;
                color: {t['ink']};
            }}

            /* Generic light card container (dipakai di beberapa halaman) */
            .plain-card {{
                background: {t['surface']};
                border: 1px solid {t['border']};
                border-radius: 14px;
                padding: 1rem;
                text-align: center;
                box-shadow: {t['shadow']};
            }}
            .plain-card .material-symbols-outlined {{ font-size: 26px; color: {t['accent']}; }}
            .plain-card .pc-title {{ font-weight: 700; margin-top: 0.3rem; color: {t['ink']}; }}
            .plain-card .pc-sub {{ font-size: 0.8rem; color: {t['muted']}; }}

            /* Legend / class card */
            .legend-card {{
                text-align:center; background:{t['surface']}; border:1px solid {t['border']};
                border-radius:12px; padding:0.9rem 0.5rem; box-shadow: {t['shadow']};
            }}
            .legend-card .legend-icon {{
                width:36px;height:36px;border-radius:9px;
                margin:0 auto 0.5rem auto; display:flex; align-items:center;
                justify-content:center; color: #ffffff;
            }}
            .legend-card .legend-label {{ font-weight:600; font-size:0.83rem; color:{t['ink']}; }}

            /* App footer */
            .app-footer {{
                text-align:center;
                color: {t['muted']};
                font-size: 0.78rem;
                padding: 1.4rem 0 0.4rem 0;
                border-top: 1px solid {t['border']};
                margin-top: 2rem;
            }}

            .stTabs [data-baseweb="tab-list"] {{ gap: 4px; }}
            .stTabs [data-baseweb="tab"] {{
                border-radius: 8px 8px 0 0;
                padding: 0.5rem 1rem;
                font-weight: 500;
                color: {t['muted']};
            }}
            .stTabs [aria-selected="true"] {{ color: {t['accent']} !important; }}

            /* Dataframe & expander container tweaks */
            [data-testid="stExpander"] {{
                border: 1px solid {t['border']} !important;
                border-radius: 12px !important;
                background: {t['surface']};
            }}
            [data-testid="stMetricValue"] {{ color: {t['ink']}; }}
            [data-testid="stMetricLabel"] {{ color: {t['muted']}; }}

            div[data-testid="stVerticalBlockBorderWrapper"] {{
                border-color: {t['border']} !important;
                background: {t['surface']};
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def theme_toggle_button():
    """Tombol untuk beralih mode terang/gelap, ditempatkan di sidebar."""
    current = get_theme_name()
    label = "Mode Gelap" if current == "light" else "Mode Terang"
    icon_name = ":material/dark_mode:" if current == "light" else ":material/light_mode:"
    st.markdown('<div class="theme-toggle-label">Tampilan</div>', unsafe_allow_html=True)
    if st.button(label, icon=icon_name, use_container_width=True, key="theme_toggle_btn"):
        toggle_theme()
        st.rerun()


def section_header(icon_name: str, title: str):
    st.markdown(
        f"""<div class="section-header">{icon(icon_name, 22)}<h3>{title}</h3></div>""",
        unsafe_allow_html=True,
    )


def page_header(eyebrow: str, title: str, sub: str, icon_name: str = None):
    icon_html = icon(icon_name, 14) if icon_name else ""
    st.markdown(
        f"""
        <div class="page-header">
            <div class="page-eyebrow">{icon_html} {eyebrow}</div>
            <div class="page-title">{title}</div>
            <div class="page-sub">{sub}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def callout(text: str):
    st.markdown(f'<div class="callout">{text}</div>', unsafe_allow_html=True)


def kpi_card(label: str, value: str, delta: str = None, delta_up: bool = True, icon_name: str = None):
    delta_html = ""
    if delta:
        cls = "kpi-delta-up" if delta_up else "kpi-delta-down"
        delta_html = f'<div class="{cls}">{delta}</div>'
    icon_html = icon(icon_name, 16) if icon_name else ""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{icon_html} {label}</div>
            <div class="kpi-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def app_footer():
    st.markdown(
        """
        <div class="app-footer">
            <strong>WebGIS Penutupan Lahan Kota Bogor</strong> &nbsp;&middot;&nbsp;
            Analisis Citra Sentinel-2 &amp; Random Forest &nbsp;&middot;&nbsp;
            Dibangun dengan Streamlit, Folium &amp; Plotly &nbsp;&middot;&nbsp;
            &copy; 2025 &mdash; Universitas Ibn Khaldun
        </div>
        """,
        unsafe_allow_html=True,
    )
