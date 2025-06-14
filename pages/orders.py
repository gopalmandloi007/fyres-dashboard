import streamlit as st
import pandas as pd
from fyres_utils import fyres_get

def show():
    st.header("Fyres Orders")
    resp = fyres_get("/api/v3/orders")
    if resp.get("s") == "ok":
        df = pd.DataFrame(resp.get("orders", []))
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No orders found.")
    else:
        st.error(f"Could not fetch orders: {resp.get('message','')}")
