import json
import streamlit as st
from fyers_apiv3 import fyersModel

@st.cache_resource
def get_fyers_client():
    with open('config1.json') as config_file:
        config = json.load(config_file)
    client_id = config['client_id']
    access_token = config['access_token']
    fyers = fyersModel.FyersModel(client_id=client_id, token=access_token)
    return fyers
