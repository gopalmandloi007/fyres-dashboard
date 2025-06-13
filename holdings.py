import streamlit as st
import pandas as pd
from utils import get_fyers_client

def show():
    st.header("FYERS Holdings")
    fyers = get_fyers_client()
    holdings = fyers.holdings()
    if holdings.get('code') == 200:
        holdings_data = holdings.get('holdings', [])
        if holdings_data:
            st.dataframe(pd.DataFrame(holdings_data))
        else:
            st.info("No holdings data available.")
    else:
        st.error(f"Failed to fetch holdings: {holdings.get('message', 'Unknown error')}")
