import streamlit as st
import pandas as pd
from fyres_utils import fyres_get

def show():
    st.header("Fyres Trades")
    resp = fyres_get("/api/v3/trades")
    if resp.get("s") == "ok":
        df = pd.DataFrame(resp.get("trades", []))
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No trades found.")
    else:
        st.error(f"Could not fetch trades: {resp.get('message','')}")
