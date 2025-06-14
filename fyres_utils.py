from fyers_apiv3 import fyersModel
import streamlit as st

@st.cache_resource
def get_fyers():
    client_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

def place_single_order(order_data):
    fyers = get_fyers()
    return fyers.place_order(data=order_data)

def place_basket_orders(basket_data):
    fyers = get_fyers()
    return fyers.place_basket_orders(data=basket_data)
