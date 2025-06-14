import requests
import streamlit as st

def get_auth_headers():
    app_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return {
        "Authorization": f"{app_id}:{access_token}",
        "Content-Type": "application/json"
    }

def fyres_place_order(
    symbol: str,
    qty: int,
    order_type: int,
    side: int,
    product_type: str,
    limit_price: float = 0.0,
    stop_price: float = 0.0,
    disclosed_qty: int = 0,
    validity: str = "DAY",
    offline_order: bool = False,
    stop_loss: float = 0.0,
    take_profit: float = 0.0,
    order_tag: str = ""
):
    url = "https://api-t1.fyers.in/api/v3/orders"
    data = {
        "symbol": symbol,
        "qty": qty,
        "type": order_type,
        "side": side,
        "productType": product_type,
        "limitPrice": float(limit_price),
        "stopPrice": float(stop_price),
        "disclosedQty": int(disclosed_qty),
        "validity": validity,
        "offlineOrder": bool(offline_order),
        "stopLoss": float(stop_loss),
        "takeProfit": float(take_profit)
    }
    if order_tag:
        data["orderTag"] = order_tag

    headers = get_auth_headers()
    resp = requests.post(url, json=data, headers=headers)
    try:
        return resp.json()
    except Exception:
        return {"s": "error", "message": "Could not decode JSON", "raw": resp.text}
