import streamlit as st
import pandas as pd
from fyres_utils import fyres_get

def show():
    st.header("Fyres Positions")
    resp = fyres_get("/api/v3/positions")
    if resp.get("s") == "ok":
        df = pd.DataFrame(resp.get("netPositions", []))
        if not df.empty:
            st.dataframe(df)
        else:
            st.info("No positions found.")
    else:
        st.error(f"Could not fetch positions: {resp.get('message','')}")
