import streamlit as st
import pandas as pd
from fyres_utils import fyres_get

def show():
    st.header("Fyres Holdings")
    resp = fyres_get("/api/v3/holdings")
    if resp.get("s") == "ok":
        df = pd.DataFrame(resp.get("holdings", []))
        if not df.empty:
            st.dataframe(df)
            st.write(f"Total P&L: {resp.get('total_pl')}, P&L%: {resp.get('pnl_perc')}%")
        else:
            st.info("No holdings found.")
    else:
        st.error("Could not fetch holdings.")
