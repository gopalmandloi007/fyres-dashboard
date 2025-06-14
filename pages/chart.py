import streamlit as st
import pandas as pd
import plotly.graph_objs as go
from fyres_utils import fyres_get

def show():
    st.header("Fyres Chart Demo")
    symbol = st.text_input("Symbol", value="NSE:SBIN-EQ")
    interval = st.selectbox(
        "Interval",
        ["D", "1", "3", "5", "15", "30", "60", "120", "240"],
        index=0
    )
    from_date = st.date_input("From date", value=pd.to_datetime("2024-01-01"))
    to_date = st.date_input("To date", value=pd.to_datetime("today"))
    if st.button("Show Chart"):
        params = {
            "symbol": symbol,
            "resolution": interval,
            "date_format": 1,
            "range_from": str(from_date),
            "range_to": str(to_date),
            "cont_flag": "",
        }
        resp = fyres_get("/data/history", params)
        st.write(resp)  # Show raw for debugging
        if resp.get("s") == "ok":
            candles = resp.get('candles', [])
            if candles:
                df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
                df["datetime"] = pd.to_datetime(df["timestamp"], unit="s")
                fig = go.Figure(data=[go.Candlestick(
                    x=df["datetime"],
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
