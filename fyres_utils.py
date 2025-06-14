from fyers_apiv3 import fyersModel
import streamlit as st

# Only one get_fyers function and cache it
@st.cache_resource
def get_fyers():
    client_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

# Order placement (single)
def place_single_order(order_data):
    fyers = get_fyers()
    return fyers.place_order(data=order_data)

# Basket order placement
def place_basket_orders(basket_data):
    fyers = get_fyers()
    return fyers.place_basket_orders(data=basket_data)

# Fetch holdings
def fetch_holdings():
    fyers = get_fyers()
    return fyers.holdings()

# --- Add more utility functions here for other API endpoints as needed ---

# Example: Fetch orders
def fetch_orders():
    fyers = get_fyers()
    return fyers.orders()

# Example: Fetch positions
def fetch_positions():
    fyers = get_fyers()
    return fyers.positions()
def fetch_positions():
    fyers = get_fyers()
    return fyers.positions()

def fetch_trades():
    fyers = get_fyers()
    return fyers.tradebook()    

def fetch_orders():
    fyers = get_fyers()
    return fyers.orderbook()

# Place GTT (Single or OCO: just change the data structure you pass)
def place_gtt_order(order_data):
    fyers = get_fyers()
    return fyers.place_gtt_order(data=order_data)

# Modify GTT Order
def modify_gtt_order(order_id, order_info):
    fyers = get_fyers()
    data = {
        "id": order_id,
        "orderInfo": order_info
    }
    return fyers.modify_gtt_order(data=data)

# Cancel GTT Order
def cancel_gtt_order(order_id):
    fyers = get_fyers()
    data = {"id": order_id}
    return fyers.cancel_gtt_order(data=data)

# Fetch GTT Order Book (all GTT orders)
def fetch_gtt_orders():
    fyers = get_fyers()
    return fyers.gtt_orderbook()
