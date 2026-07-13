import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import (
    load_change_matrix, load_classification_report,
    load_confusion_matrix, load_feature_importance, CLASS_ORDER,
)
from utils.style import section_header, callout, page_header, style_plot, get_theme


def render():
    theme = get_theme()
    page_header(
        eyebrow="Visualisasi",
        title="Visualisasi & Evaluasi Model",
        sub="Matriks perubahan kelas, evaluasi akurasi model, dan tingkat kepentingan fitur.",
        icon_name="insights",
    )

    tab1, tab2, tab3 = st.tabs([
        "Matriks Perubahan Kelas",
        "Evaluasi Akurasi Model",
        "Kepentingan Fitur",
    ])

    # ---------- TAB 1: Matriks Perubahan ----------
    with tab1:
        callout(
            "Matriks ini menunjukkan luas transisi antar kelas penutupan lahan "
            "dari tahun 2020 (baris) ke tahun 2021 (kolom), dalam satuan jumlah piksel. "
            "Diagonal menunjukkan area yang <b>tidak berubah kelas</b>."
        )
        try:
            cm = load_change_matrix()
        except Exception as e:
            st.error(f"Gagal memuat matriks perubahan: {e}")
            cm = None

        if cm is not None:
            fig_heat = go.Figure(data=go.Heatmap(
                z=cm.values, x=cm.columns, y=cm.index,
                colorscale="Teal", text=cm.values, texttemplate="%{text}",
                textfont={"size": 10}, hovertemplate="Dari %{y} → %{x}<br>Jumlah piksel: %{z}<extra></extra>",
            ))
            fig_heat.update_layout(
                height=420, margin=dict(l=10, r=10, t=20, b=10),
                xaxis_title="Kelas 2021", yaxis_title="Kelas 2020",
            )
            st.plotly_chart(style_plot(fig_heat), use_container_width=True, theme=None)

            with st.expander("Lihat tabel mentah matriks perubahan", icon=":material/table_chart:", expanded=False):
                st.dataframe(cm.style.background_gradient(cmap="Blues", axis=None), use_container_width=True)

            st.markdown("##### Interpretasi")
            diag_total = sum(cm.iloc[i, i] for i in range(min(len(cm), len(cm.columns))) if cm.index[i] in cm.columns)
            total_all = cm.values.sum()
            persist_pct = diag_total / total_all * 100 if total_all else 0
            st.info(
                f"Sekitar **{persist_pct:.1f}%** dari total area tidak mengalami perubahan kelas "
                f"antara tahun 2020 dan 2021 (nilai diagonal matriks).",
                icon=":material/query_stats:",
            )

    # ---------- TAB 2: Evaluasi Model ----------
    with tab2:
        callout(
            "Evaluasi performa model klasifikasi <b>Random Forest</b> berdasarkan data uji "
            "(validasi lapangan), meliputi classification report dan confusion matrix."
        )

        try:
            report = load_classification_report()
        except Exception as e:
            report = None
            st.error(f"Gagal memuat classification report: {e}")

        if report is not None:
            report_display = report.copy()
            rename_map = {str(i + 1): kelas for i, kelas in enumerate(CLASS_ORDER)}
            report_display.index = [rename_map.get(str(idx), str(idx)) for idx in report_display.index]

            acc_row = None
            for idx in report_display.index:
                if idx.lower() == "accuracy":
                    acc_row = report_display.loc[idx, "precision"]
                    break

            c1, c2 = st.columns([1.3, 1])
            with c1:
                st.markdown("##### Classification Report")
                st.dataframe(
                    report_display.style.format("{:.3f}").background_gradient(cmap="Greens", axis=None),
                    use_container_width=True, height=320,
                )
            with c2:
                if acc_row is not None:
                    st.metric("Akurasi Keseluruhan", f"{acc_row * 100:.2f}%")
                st.markdown(
                    "**Precision**: proporsi prediksi benar dari seluruh prediksi suatu kelas.\n\n"
                    "**Recall**: proporsi data aktual suatu kelas yang berhasil diprediksi benar.\n\n"
                    "**F1-score**: rata-rata harmonik precision dan recall."
                )

        st.markdown("##### Confusion Matrix")
        try:
            conf = load_confusion_matrix()
            conf.index = CLASS_ORDER[: len(conf)]
            conf.columns = CLASS_ORDER[: len(conf.columns)]
            fig_conf = go.Figure(data=go.Heatmap(
                z=conf.values, x=conf.columns, y=conf.index,
                colorscale="Oranges", text=conf.values, texttemplate="%{text}",
                textfont={"size": 11}, hovertemplate="Aktual %{y} — Prediksi %{x}: %{z}<extra></extra>",
            ))
            fig_conf.update_layout(
                height=420, margin=dict(l=10, r=10, t=20, b=10),
                xaxis_title="Kelas Prediksi", yaxis_title="Kelas Aktual",
            )
            st.plotly_chart(style_plot(fig_conf), use_container_width=True, theme=None)
            st.caption("Nilai pada diagonal menunjukkan jumlah sampel yang diklasifikasikan dengan benar.")
        except Exception as e:
            st.error(f"Gagal memuat confusion matrix: {e}")

    # ---------- TAB 3: Feature Importance ----------
    with tab3:
        callout(
            "Grafik ini menunjukkan tingkat kepentingan (feature importance) tiap band "
            "spektral / indeks yang digunakan model Random Forest dalam proses klasifikasi."
        )
        try:
            fi = load_feature_importance()
        except Exception as e:
            fi = None
            st.error(f"Gagal memuat feature importance: {e}")

        if fi is not None:
            fig_fi = px.bar(
                fi, x="importance", y="feature", orientation="h",
                color="importance", color_continuous_scale="Teal",
                labels={"importance": "Tingkat Kepentingan", "feature": "Fitur"},
                height=460,
            )
            fig_fi.update_layout(margin=dict(l=10, r=10, t=20, b=10), yaxis=dict(autorange="reversed"))
            st.plotly_chart(style_plot(fig_fi), use_container_width=True, theme=None)

            top3 = fi.head(3)["feature"].tolist()
            st.info(f"Tiga fitur paling berpengaruh dalam klasifikasi: **{', '.join(top3)}**.", icon=":material/lightbulb:")
