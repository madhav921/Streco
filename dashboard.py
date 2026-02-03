import streamlit as st
import pandas as pd
import json
import config as cg
import data.market_data as mkt_data
import indicators.metadata as md
from strategies.recommender import get_top_stocks
from stock_names import STOCK_NAMES
import os
from datetime import datetime
import plotly.graph_objects as go

# ===============================
# PAGE CONFIG
# ===============================
st.set_page_config(
    page_title="Streco AI Trading Dashboard",
    layout="wide",
    page_icon="📈"
)

# ===============================
# COOL UI HEADER
# ===============================
st.markdown("""
<style>
.big-title {
    font-size:42px;
    font-weight:bold;
    color:#00ffaa;
    animation: glow 2s ease-in-out infinite alternate;
}
@keyframes glow {
    from { text-shadow: 0 0 10px #00ffaa; }
    to { text-shadow: 0 0 25px #00ffcc; }
}
</style>
<div class="big-title">🚀 Streco Quant Stock Recommendation System</div>
""", unsafe_allow_html=True)

# Sidebar
page = st.sidebar.radio("📊 Navigation", ["Stock Recommendations", "Metadata Explorer"])

# ===============================
# PAGE 1: STOCK RECOMMENDATIONS
# ===============================
if page == "Stock Recommendations":
    st.subheader("🔥 Top Stocks to Invest (Quant Score)")

    # Load cached results
    try:
        with open("latest_recommendations.json") as f:
            data = json.load(f)
    except:
        st.error("No recommendation data found. Scheduler not run yet.")
        st.stop()

    timestamp = data["timestamp"]
    stocks = data["stocks"]

    # Show timestamp on top right
    st.markdown(f"<div style='text-align:right;color:gray;'>Last Updated: {timestamp} IST</div>", unsafe_allow_html=True)

    rec_df = pd.DataFrame(stocks)
    st.dataframe(rec_df, width="stretch")

    st.subheader("📊 Score Visualization")
    st.bar_chart(rec_df.set_index("name")["score"])
# ===============================
# PAGE 2: METADATA EXPLORER (PARQUET + CHART)
# ===============================
if page == "Metadata Explorer":
    st.subheader("🔬 Stock Metadata Explorer (Cached Parquet)")

    symbol = st.selectbox("Select Stock", list(STOCK_NAMES.keys()))
    file_path = f"metadata/{symbol}.parquet"

    # Show global update time
    if os.path.exists("metadata/last_updated.txt"):
        with open("metadata/last_updated.txt") as f:
            last_time = f.read()
        st.markdown(f"<div style='text-align:right;color:gray;'>Last Updated: {last_time} IST</div>", unsafe_allow_html=True)

    if not os.path.exists(file_path):
        st.error(f"No metadata found for {symbol}. Run main.py first.")
        st.stop()

    # Load parquet
    df = pd.read_parquet(file_path)
    st.success(f"Loaded cached metadata for {symbol}")

    # =========================
    # INTERACTIVE CANDLE CHART
    # =========================
    st.subheader("📈 Interactive Trading Chart")

    # Ensure datetime index
    if "Datetime" in df.columns:
        df["Datetime"] = pd.to_datetime(df["Datetime"])
        df.set_index("Datetime", inplace=True)

    # Plotly Candlestick Chart
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df["Open"],
        high=df["High"],
        low=df["Low"],
        close=df["Close"],
        name="Price"
    ))

    # Moving Averages
    if "ma20" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["ma20"], line=dict(color="blue"), name="MA20"))
    if "ma50" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["ma50"], line=dict(color="orange"), name="MA50"))
    if "ma200" in df.columns:
        fig.add_trace(go.Scatter(x=df.index, y=df["ma200"], line=dict(color="red"), name="MA200"))

    # Volume subplot
    fig.add_trace(go.Bar(
        x=df.index,
        y=df["Volume"],
        name="Volume",
        yaxis="y2",
        opacity=0.3
    ))

    # Layout (TradingView style)
    fig.update_layout(
        title=f"{symbol} Price Chart",
        xaxis_rangeslider_visible=True,
        yaxis=dict(title="Price"),
        yaxis2=dict(overlaying="y", side="right", title="Volume", showgrid=False),
        template="plotly_dark",
        height=700
    )

    st.plotly_chart(fig, use_container_width=True)

    # =========================
    # SHOW METADATA TABLE
    # =========================
    st.subheader("📊 Latest Metadata (Last 200 Rows)")
    st.dataframe(df.tail(200), width="stretch")
