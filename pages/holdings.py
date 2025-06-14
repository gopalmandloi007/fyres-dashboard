import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from fyres_utils import fetch_holdings

def show():
    st.header("Fyers Holdings")

    resp = fetch_holdings()
    if resp.get("s") == "ok":
        holdings = resp.get("holdings", [])
        overall = resp.get("overall", {})

        if holdings:
            df = pd.DataFrame(holdings)
            # Rearranging columns for better display (optional)
            display_cols = [
                "symbol", "holdingType", "quantity", "remainingQuantity", "qty_t1",
                "costPrice", "marketVal", "ltp", "pl", "collateralQuantity", "remainingPledgeQuantity", "isin"
            ]
            display_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[display_cols])

            st.markdown(
                f"""**Total Holdings:** {overall.get('count_total',0)}  
**Invested Amount:** ₹{overall.get('total_investment',0):,.2f}  
**Current Value:** ₹{overall.get('total_current_value',0):,.2f}  
**Total P&L:** ₹{overall.get('total_pl',0):,.2f}  
**P&L %:** {overall.get('pnl_perc',0):.2f}%"""
            )
        else:
            st.info("No holdings found.")
    else:
        st.error(f"Could not fetch holdings: {resp.get('message', '')}")

if __name__ == "__main__":
    show()
