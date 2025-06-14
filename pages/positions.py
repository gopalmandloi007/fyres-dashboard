import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from fyres_utils import fetch_positions

def show():
    st.header("Fyers Positions")
    resp = fetch_positions()
    if resp.get("s") == "ok":
        positions = resp.get("netPositions", []) or resp.get("positions", [])  # API may use either key
        overall = resp.get("overall", {})

        if positions:
            df = pd.DataFrame(positions)
            display_cols = [
                "symbol", "productType", "side", "netQty", "netAvg", "pl", "realized_profit",
                "buyQty", "buyAvg", "sellQty", "sellAvg", "ltp", "segment", "exchange"
            ]
            display_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[display_cols])

            st.markdown(
                f"""**Total Positions:** {overall.get('count_total', 0)}  
**Open Positions:** {overall.get('count_open', 0)}  
**Total P&L:** ₹{overall.get('pl_total', 0):,.2f}  
**Realized P&L:** ₹{overall.get('pl_realized', 0):,.2f}  
**Unrealized P&L:** ₹{overall.get('pl_unrealized', 0):,.2f}"""
            )
        else:
            st.info("No open/closed positions for today.")
    else:
        st.error(f"Could not fetch positions: {resp.get('message', '')}")

if __name__ == "__main__":
    show()
