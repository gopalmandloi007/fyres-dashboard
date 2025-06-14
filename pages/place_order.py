import streamlit as st
from fyres_utils import fyres_post

def show():
    st.header("Place Normal Order")
    symbol = st.text_input("Symbol", "NSE:SBIN-EQ")
    qty = st.number_input("Quantity", min_value=1, step=1)
    side = st.selectbox("Side", [("Buy", 1), ("Sell", -1)], format_func=lambda x: x[0])[1]
    order_type = st.selectbox("Order Type", [("Limit", 1), ("Market", 2), ("Stop (SL-M)", 3), ("Stoplimit (SL-L)", 4)], format_func=lambda x:x[0])[1]
    product_type = st.selectbox("Product Type", ["CNC", "INTRADAY", "MARGIN", "CO", "BO", "MTF"])
    limit_price = st.number_input("Limit Price", value=0.0)
    stop_price = st.number_input("Stop Price", value=0.0)
    disclosed_qty = st.number_input("Disclosed Qty (Equity only)", min_value=0, step=1)
    validity = st.selectbox("Order Validity", ["DAY", "IOC"])
    offline_order = st.checkbox("AMO Order (place when market closed)", value=False)
    stop_loss = st.number_input("Stop Loss (for CO/BO)", value=0.0)
    take_profit = st.number_input("Take Profit (for BO)", value=0.0)
    order_tag = st.text_input("Order Tag (optional, no spaces/special chars except _)", "")

    if st.button("Place Order"):
        data = {
            "symbol": symbol,
            "qty": int(qty),
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
        resp = fyres_post("/api/v3/orders", data)
        st.write("API Raw Response:", resp)
        if resp.get("s") == "ok":
            st.success(f"Order placed! Ref: {resp.get('id')}")
        else:
            st.error(f"Order failed: {resp.get('message') or resp.get('raw') or resp}")
