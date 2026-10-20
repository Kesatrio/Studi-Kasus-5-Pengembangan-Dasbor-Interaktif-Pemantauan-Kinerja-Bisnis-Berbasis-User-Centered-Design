import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
st.set_page_config(
    page_title="Executive KPI Dashboard",
    page_icon="📊",
    layout="wide"
)
st.markdown("""
    <style>
    .main { background-color: #FAFAFA; }
    div[data-testid="stMetricValue"] { font-size: 28px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)
@st.cache_data
def load_data():
    np.random.seed(42)
    dates = pd.date_range(start="2026-01-01", periods=120, freq="D")
    regions = ["Jakarta", "Bandung", "Surabaya", "Medan"]
    
    data = []
    for d in dates:
        for r in regions:
            sales = np.random.randint(100, 500) + (10 if r == "Jakarta" else 0)
            target = 300
            data.append([d, r, sales, target])
            
    df = pd.DataFrame(data, columns=["Tanggal", "Wilayah", "Penjualan", "Target"])
    return df

df = load_data()
st.title("📊 Monitoring KPI Penjualan Harian")
st.caption("Penerapan Prinsip HCI & Data-Ink Ratio Edward Tufte")
col_filter1, col_filter2 = st.columns([2, 2])
with col_filter1:
    selected_region = st.selectbox("Pilih Wilayah:", ["Semua Wilayah"] + list(df["Wilayah"].unique()))
with col_filter2:
    date_range = st.date_input("Rentang Tanggal:", [df["Tanggal"].min(), df["Tanggal"].max()])
filtered_df = df.copy()
if selected_region != "Semua Wilayah":
    filtered_df = filtered_df[filtered_df["Wilayah"] == selected_region]

filtered_df = filtered_df[
    (filtered_df["Tanggal"] >= pd.to_datetime(date_range[0])) & 
    (filtered_df["Tanggal"] <= pd.to_datetime(date_range[1]))
]
total_sales = filtered_df["Penjualan"].sum()
total_target = filtered_df["Target"].sum()
achievement = (total_sales / total_target) * 100

m1, m2, m3 = st.columns(3)
m1.metric("Total Penjualan", f"Rp {total_sales:,.0f}")
m2.metric("Target", f"Rp {total_target:,.0f}")
m3.metric("Capaian Target", f"{achievement:.1f}%", delta=f"{achievement - 100:.1f}%")
st.divider()
col_chart1, col_chart2 = st.columns([3, 2])
with col_chart1:
    st.subheader("Tren Penjualan Harian")
    fig_line = px.line(
        filtered_df.groupby("Tanggal")["Penjualan"].sum().reset_index(),
        x="Tanggal",
        y="Penjualan",
        labels={"Penjualan": "Total Unit", "Tanggal": "Tanggal"},
        template="plotly_white"
    )
    fig_line.update_xaxes(showgrid=False)
    fig_line.update_traces(line_color="#1E88E5", line_width=2.5)
    st.plotly_chart(fig_line, use_container_width=True)

with col_chart2:
    st.subheader("Perbandingan Per Wilayah")
    region_summary = filtered_df.groupby("Wilayah")["Penjualan"].sum().reset_index()
    fig_bar = px.bar(
        region_summary,
        x="Wilayah",
        y="Penjualan",
        color="Penjualan",
        color_continuous_scale="Blues",
        template="plotly_white"
    )
    fig_bar.update_layout(coloraxis_showscale=False)
    st.plotly_chart(fig_bar, use_container_width=True)
with st.expander("🔍 Lihat Detail Data Transaksi (Details on Demand)"):
    st.dataframe(filtered_df, use_container_width=True)
