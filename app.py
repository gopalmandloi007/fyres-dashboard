import streamlit as st
import importlib

st.set_page_config(page_title="Fyres Dashboard", layout="wide")

PAGES = {
    "Holdings": "holdings",
    "Positions": "positions",
    "Orders": "orders",
    "Trades": "trades",
    "GTT": "gtt",
    "Charts": "chart",
    "Place Order": "place_order",
    "GTT Order": "place_gtt",
    "Modify/Cancel Order": "modify_cancel_order",
    "Modify/Cancel GTT": "modify_cancel_gtt",
}

st.sidebar.title("Fyres Dashboard")
page = st.sidebar.radio("Go to", list(PAGES.keys()))
modulename = PAGES[page]
module = importlib.import_module(f"pages.{modulename}")
module.show()
