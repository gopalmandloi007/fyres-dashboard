from fyers_apiv3 import fyersModel
import streamlit as st
import requests

import streamlit as st

def debug_secrets():
    st.write(st.secrets)

# Cached Fyers object
@st.cache_resource
def get_fyers():
    client_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

# --- SDK Wrappers ---

def place_single_order(order_data):
    fyers = get_fyers()
    return fyers.place_order(data=order_data)

def place_basket_orders(basket_data):
    fyers = get_fyers()
    return fyers.place_basket_orders(data=basket_data)

def fetch_holdings():
    fyers = get_fyers()
    return fyers.holdings()

def fetch_orders():
    fyers = get_fyers()
    return fyers.orderbook()

def fetch_positions():
    fyers = get_fyers()
    return fyers.positions()

def fetch_trades():
    fyers = get_fyers()
    return fyers.tradebook()    

def place_gtt_order(order_data):
    fyers = get_fyers()
    return fyers.place_gtt_order(data=order_data)

def modify_gtt_order(order_id, order_info):
    fyers = get_fyers()
    data = {
        "id": order_id,
        "orderInfo": order_info
    }
    return fyers.modify_gtt_order(data=data)

def cancel_gtt_order(order_id):
    fyers = get_fyers()
    data = {"id": order_id}
    return fyers.cancel_gtt_order(data=data)

def fetch_gtt_orders():
    fyers = get_fyers()
    return fyers.gtt_orderbook()

# --- REST API helpers (for endpoints not covered by SDK, e.g. chart/history) ---

def get_fyers_access_token():
    return st.secrets["fyres_access_token"]

def fyres_get(endpoint, params=None):
    url = "https://api-t1.fyers.in" + endpoint
    headers = {"Authorization": get_fyers_access_token()}
    resp = requests.get(url, headers=headers, params=params)
    return resp.json()

def fyres_patch(endpoint, data):
    url = "https://api-t1.fyers.in" + endpoint
    headers = {"Authorization": get_fyers_access_token()}
    resp = requests.patch(url, headers=headers, json=data)
    return resp.json()

def fyres_delete(endpoint, data):
    url = "https://api-t1.fyers.in" + endpoint
    headers = {"Authorization": get_fyers_access_token()}
    resp = requests.delete(url, headers=headers, json=data)
    return resp.json()
