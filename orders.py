import streamlit as st
import pandas as pd
from utils import get_fyers_client

def show():
    st.header("Order Book (FYERS)")
    fyers = get_fyers_client()
    orders = fyers.orderbook()
    if orders['code'] == 200:
        orders_data = orders.get('orderBook', [])
        if orders_data:
            df = pd.DataFrame(orders_data)
            st.dataframe(df)
        else:
            st.info("No orders data available.")
    else:
        st.error(f"Error fetching orders: {orders.get('message', 'No message available')}")
