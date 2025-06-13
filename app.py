import streamlit as st
import importlib

st.set_page_config(page_title="FYERS Integrate Dashboard", layout="wide")
st.title("FYERS Integrate Dashboard")

PAGES = {
    "Holdings": "holdings",
    "Orders": "orders",
    "Order Manage": "order_manage",
    "Place Order": "place_order",
}

page = st.sidebar.radio("Go to", list(PAGES.keys()))
modulename = PAGES[page]

try:
    module = importlib.import_module(modulename)
    if hasattr(module, "show"):
        module.show()
    else:
        st.error(f"Module `{modulename}` missing `show()` function.")
except ModuleNotFoundError:
    st.error(f"Module `{modulename}.py` not found.")
except Exception as e:
    st.error(f"Error loading `{modulename}`: {e}")
