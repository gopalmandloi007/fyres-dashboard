import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from fyres_utils import fyres_get

def show():
    st.header("Fyres Chart Demo")
    symbol = st.text_input("Symbol", value="NSE:SBIN-EQ")
    interval = st.selectbox("Interval", ["1", "3", "5", "15", "30", "60", "D"], index=6)
    if st.button("Show Chart"):
        params = {
            "symbol": symbol,
            "resolution": interval,
            "date_format": "1",
            "range_from": "2024-06-01",
            "range_to": "2024-06-14"
        }
        resp = fyres_get("/api/v3/history", params)
        if resp.get("s") == "ok":
            candles = resp.get('candles', [])
            if candles:
                df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
                fig = go.Figure(data=[go.Candlestick(
                    x=pd.to_datetime(df["timestamp"], unit="s"),
                    open=df["open"],
                    high=df["high"],
                    low=df["low"],
                    close=df["close"]
                )])
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.warning("No candle data.")
        else:
            st.error(f"Failed to get candles: {resp.get('message','')}")
