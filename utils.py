import streamlit as st
from fyers_apiv3 import fyersModel

@st.cache_resource
def get_fyers_client():
    client_id = st.secrets["fyers_client_id"]
    access_token = st.secrets["fyers_access_token"]
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
    return fyers
