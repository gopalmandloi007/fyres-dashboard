import streamlit as st
import pandas as pd
from fyres_utils import fyres_get, fyres_post, fyres_patch, fyres_delete

def show():
    st.header("Fyres GTT Orders")
    resp = fyres_get("/api/v3/gtt/orders")
    if resp.get("s") == "ok":
        df = pd.DataFrame(resp.get("orderBook", []))
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No GTT orders found.")
    else:
        st.error(f"Could not fetch GTT orders: {resp.get('message','')}")
