from fyres_utils import debug_secrets
debug_secrets()  # sirf debugging ke liye, baad me hata dena

import streamlit as st
import pandas as pd
from fyres_utils import fetch_orders

def show():
    st.header("Fyers Orders")
    resp = fetch_orders()
    if resp.get("s") == "ok":
        orders = resp.get("orderBook", []) or resp.get("orders", [])
        if orders:
            df = pd.DataFrame(orders)
            display_cols = [
                "symbol", "qty", "type", "side", "productType", "limitPrice", "stopPrice",
                "status", "orderDateTime", "filledQty", "disclosedQty", "orderTag", "id"
            ]
            display_cols = [col for col in display_cols if col in df.columns]
            st.dataframe(df[display_cols] if display_cols else df)
        else:
            st.info("No orders found.")
    else:
        st.error(f"Could not fetch orders: {resp.get('message','')}")

if __name__ == "__main__":
    show()
