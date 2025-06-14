from fyers_apiv3 import fyersModel
import streamlit as st

@st.cache_resource
def get_fyers():
    client_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return fyersModel.FyersModel(client_id=client_id, token=access_token, is_async=False, log_path="")

def debug_secrets():
    st.write("Secrets loaded:", dict(st.secrets))

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

def fyres_get(endpoint, params):
    fyers = get_fyers()
    # 'endpoint' can be used to select the API method; here, we just handle "/data/history" as you used in chart.py
    if endpoint == "/data/history":
        return fyers.history(params)
    # Add more endpoints if needed
    return {"s": "error", "message": f"Unknown endpoint {endpoint}"}

def fyres_patch(endpoint, data):
    fyers = get_fyers()
    # For order modification, as in modify_cancel_order.py
    if endpoint == "/api/v3/orders/sync":
        return fyers.modify_order(data=data)
    return {"s": "error", "message": f"Unknown endpoint {endpoint}"}

def fyres_delete(endpoint, data):
    fyers = get_fyers()
    # For order cancel, as in modify_cancel_order.py
    if endpoint == "/api/v3/orders/sync":
        return fyers.cancel_order(data=data)
    return {"s": "error", "message": f"Unknown endpoint {endpoint}"}

def squareoff_positions(ids=None):
    """
    ids: list of position ids to square off, or None to square off all
    """
    fyers = get_fyers()
    data = {}
    if ids:
        data["id"] = ids
    # API name is assumed, replace with actual if different
    return fyers.exit_positions(data=data)

def sell_holding(symbol, qty, order_type, limit_price=None):
    """
    symbol: string (e.g. NSE:SBIN-EQ)
    qty: int
    order_type: 2 for Market, 1 for Limit
    limit_price: required if order_type==1
    """
    fyers = get_fyers()
    order_data = {
        "symbol": symbol,
        "qty": int(qty),
        "type": order_type,
        "side": -1,  # Sell
        "productType": "CNC",  # Usually for holdings
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "hold-exit"
    }
    if order_type == 1:  # Limit
        order_data["limitPrice"] = float(limit_price)
    else:
        order_data["limitPrice"] = 0
    order_data["stopPrice"] = 0
    return fyers.place_order(data=order_data)
