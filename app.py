import streamlit as st
import importlib

st.set_page_config(page_title="Fyres Dashboard", layout="wide")

PAGES = {
    "Holdings": "holdings",
    "Positions": "positions",
    "Orders": "orders",
    "Trades": "trades",
    "GTT": "gtt",
    "Charts": "chart"
}

st.sidebar.title("Fyres Dashboard")
page = st.sidebar.radio("Go to", list(PAGES.keys()))
modulename = PAGES[page]
module = importlib.import_module(f"pages.{modulename}")
module.show()
