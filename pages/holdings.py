import streamlit as st
import pandas as pd
from fyres_utils import fetch_holdings

def show():
    st.header("Fyers Holdings")
    resp = fetch_holdings()
    if resp.get("s") == "ok":
        df = pd.DataFrame(resp.get("holdings", []))
        if not df.empty:
            st.dataframe(df)
            total_pl = resp.get("overall_pl", None) or resp.get("total_pl", None)
            pnl_perc = resp.get("overall_pl_perc", None) or resp.get("pnl_perc", None)
            st.markdown(
                f"**Total P&L:** {total_pl if total_pl is not None else 0} | **P&L %:** {pnl_perc if pnl_perc is not None else 0}%"
            )
        else:
            st.info("No holdings found.")
    else:
        st.error(f"Could not fetch holdings: {resp.get('message', '')}")

if __name__ == "__main__":
    show()
