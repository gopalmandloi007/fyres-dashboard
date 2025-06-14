import streamlit as st
import pandas as pd
from fyres_utils import fetch_gtt_orders

def show():
    st.header("Fyers GTT Order Book")
    resp = fetch_gtt_orders()
    if resp.get("s") == "ok":
        orders = resp.get("orderBook", [])
        if orders:
            df = pd.DataFrame(orders)
            # You can customize columns below as per your needs
            display_cols = [
                "id", "symbol", "product_type", "qty", "price_limit", "price_trigger",
                "qty2", "price2_limit", "price2_trigger", "ord_status", "report_type", "create_time"
            ]
            display_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[display_cols] if display_cols else df)
        else:
            st.info("No GTT orders found.")
    else:
        st.error(f"Could not fetch GTT orders: {resp.get('message','')}")

if __name__ == "__main__":
    show()
