import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from fyres_utils import fetch_trades

def show():
    st.header("Fyers Trades")
    resp = fetch_trades()
    if resp.get("s") == "ok":
        trades = resp.get("tradeBook", []) or resp.get("trades", [])  # API may use either key

        if trades:
            df = pd.DataFrame(trades)
            display_cols = [
                "symbol", "orderDateTime", "tradedQty", "tradePrice", "tradeValue", "side",
                "orderNumber", "tradeNumber", "productType", "segment", "exchange", "orderTag"
            ]
            display_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[display_cols])
            st.info(f"Total Trades Today: {len(df)}")
        else:
            st.info("No trades found for today.")
    else:
        st.error(f"Could not fetch trades: {resp.get('message', '')}")

if __name__ == "__main__":
    show()
