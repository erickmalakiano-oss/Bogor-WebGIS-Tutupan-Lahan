import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import load_luas_stats
from utils.style import section_header, callout, kpi_card, page_header, style_plot, get_theme, CLASS_COLORS


def render():
    theme = get_theme()
    page_header(
        eyebrow="Statistik",
        title="Statistik Penutupan Lahan (2020 — 2021)",
        sub="Ringkasan luas dan perubahan tiap kelas penutupan lahan hasil klasifikasi citra.",
        icon_name="bar_chart",
    )

    try:
        df = load_luas_stats()
    except Exception as e:
        st.error(f"Gagal memuat data statistik: {e}")
        return

    total_2020 = df["2020"].sum()
    total_2021 = df["2021"].sum()
    kelas_naik = df["Perubahan"].idxmax()
    kelas_turun = df["Perubahan"].idxmin()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Total Luas 2020", f"{total_2020:,.2f} ha", icon_name="calendar_month")
    with c2:
        delta = total_2021 - total_2020
        kpi_card("Total Luas 2021", f"{total_2021:,.2f} ha", f"{delta:+.2f} ha", delta_up=(delta >= 0), icon_name="calendar_month")
    with c3:
        kpi_card("Kenaikan Terbesar", kelas_naik, f"{df.loc[kelas_naik,'Perubahan']:+.2f} ha", delta_up=True, icon_name="trending_up")
    with c4:
        kpi_card("Penurunan Terbesar", kelas_turun, f"{df.loc[kelas_turun,'Perubahan']:+.2f} ha", delta_up=False, icon_name="trending_down")

    st.write("")

    tab1, tab2, tab3 = st.tabs(["Ringkasan", "Analisis Perubahan", "Data & Unduh"])

    # ---------- TAB 1 ----------
    with tab1:
        callout("Nilai luas dalam satuan hektar (ha), hasil klasifikasi citra Sentinel-2 dengan algoritma Random Forest.")
        col1, col2 = st.columns([1, 1])

        with col1:
            st.markdown("##### Tabel Luas per Kelas")
            st.dataframe(
                df.style.format("{:,.2f}").background_gradient(cmap="YlGn", subset=["2020", "2021"]),
                use_container_width=True,
                height=260,
            )

        with col2:
            st.markdown("##### Perbandingan Luas 2020 vs 2021")
            df_melt = df[["2020", "2021"]].reset_index().melt(id_vars="Kelas", var_name="Tahun", value_name="Luas (ha)")
            fig = px.bar(
                df_melt, x="Kelas", y="Luas (ha)", color="Tahun", barmode="group",
                color_discrete_sequence=[theme["accent"], theme["ink"]], text_auto=".1f", height=380,
            )
            fig.update_layout(margin=dict(l=10, r=10, t=20, b=10), legend=dict(orientation="h", y=1.12))
            st.plotly_chart(style_plot(fig), use_container_width=True, theme=None)

        st.markdown("##### Proporsi Tiap Kelas")
        pc1, pc2 = st.columns(2)
        with pc1:
            fig_pie20 = px.pie(
                df.reset_index(), names="Kelas", values="2020", color="Kelas",
                color_discrete_map=CLASS_COLORS, hole=0.45, title="Tahun 2020",
            )
            fig_pie20.update_traces(textinfo="percent+label")
            st.plotly_chart(style_plot(fig_pie20), use_container_width=True, theme=None)
        with pc2:
            fig_pie21 = px.pie(
                df.reset_index(), names="Kelas", values="2021", color="Kelas",
                color_discrete_map=CLASS_COLORS, hole=0.45, title="Tahun 2021",
            )
            fig_pie21.update_traces(textinfo="percent+label")
            st.plotly_chart(style_plot(fig_pie21), use_container_width=True, theme=None)

    # ---------- TAB 2 ----------
    with tab2:
        callout("Nilai positif menunjukkan pertambahan luas, nilai negatif menunjukkan pengurangan luas kelas penutupan lahan antara 2020–2021.")

        colors = [theme["success"] if v >= 0 else theme["danger"] for v in df["Perubahan"]]
        fig_change = go.Figure(go.Bar(
            x=df["Perubahan"], y=df.index, orientation="h",
            marker_color=colors, text=df["Perubahan"].round(2), textposition="outside",
        ))
        fig_change.update_layout(
            height=380, margin=dict(l=10, r=10, t=20, b=10),
            xaxis_title="Perubahan Luas (ha)", yaxis_title="",
        )
        fig_change.add_vline(x=0, line_color=theme["muted"], line_width=1)
        st.plotly_chart(style_plot(fig_change), use_container_width=True, theme=None)

        st.markdown("##### Persentase Perubahan Relatif")
        df_pct = df.copy()
        df_pct["Perubahan (%)"] = (df_pct["Perubahan"] / df_pct["2020"] * 100).round(2)
        st.dataframe(
            df_pct[["2020", "2021", "Perubahan", "Perubahan (%)"]]
            .style.format({"2020": "{:,.2f}", "2021": "{:,.2f}", "Perubahan": "{:+.2f}", "Perubahan (%)": "{:+.2f}%"})
            .map(lambda v: f"color:{theme['success']};font-weight:600" if isinstance(v, (int, float)) and v > 0
                 else (f"color:{theme['danger']};font-weight:600" if isinstance(v, (int, float)) and v < 0 else ""),
                 subset=["Perubahan", "Perubahan (%)"]),
            use_container_width=True,
            height=240,
        )

        col_n1, col_n2 = st.columns(2)
        with col_n1:
            with st.container(border=True):
                st.success("#### Kelas Meningkat", icon=":material/trending_up:")
                naik = df[df["Perubahan"] > 0]
                if len(naik):
                    for k, row in naik.iterrows():
                        st.markdown(f"**{k}** — naik **{row['Perubahan']:+.2f} ha**")
                else:
                    st.markdown("Tidak ada kelas yang meningkat.")
        with col_n2:
            with st.container(border=True):
                st.error("#### Kelas Menurun", icon=":material/trending_down:")
                turun = df[df["Perubahan"] < 0]
                if len(turun):
                    for k, row in turun.iterrows():
                        st.markdown(f"**{k}** — turun **{row['Perubahan']:+.2f} ha**")
                else:
                    st.markdown("Tidak ada kelas yang menurun.")

    # ---------- TAB 3 ----------
    with tab3:
        st.markdown("##### Data Lengkap")
        st.dataframe(df.style.format("{:,.2f}"), use_container_width=True, height=240)

        csv_bytes = df.to_csv().encode("utf-8")
        st.download_button(
            "Unduh Data Statistik (CSV)",
            data=csv_bytes,
            file_name="statistik_penutupan_lahan_2020_2021.csv",
            mime="text/csv",
            icon=":material/download:",
            use_container_width=False,
        )
