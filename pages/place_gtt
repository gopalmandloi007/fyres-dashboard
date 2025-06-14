import streamlit as st
from fyres_utils import fyres_post

def show():
    st.header("Place GTT Order (Single or OCO)")
    symbol = st.text_input("Symbol", "NSE:SBIN-EQ")
    side = st.selectbox("Side", [("Buy", 1), ("Sell", -1)], format_func=lambda x: x[0])[1]
    product_type = st.selectbox("Product Type", ["CNC", "MARGIN", "MTF"])

    order_type = st.radio("GTT Type", ["Single", "OCO"])
    leg1_price = st.number_input("Leg 1 - Price", value=0.0)
    leg1_trigger = st.number_input("Leg 1 - Trigger Price", value=0.0)
    leg1_qty = st.number_input("Leg 1 - Qty", min_value=1, step=1)

    if order_type == "OCO":
        leg2_price = st.number_input("Leg 2 - Price", value=0.0)
        leg2_trigger = st.number_input("Leg 2 - Trigger Price", value=0.0)
        leg2_qty = st.number_input("Leg 2 - Qty", min_value=1, step=1)
        order_info = {
            "leg1": {"price": float(leg1_price), "triggerPrice": float(leg1_trigger), "qty": int(leg1_qty)},
            "leg2": {"price": float(leg2_price), "triggerPrice": float(leg2_trigger), "qty": int(leg2_qty)},
        }
    else:
        order_info = {
            "leg1": {"price": float(leg1_price), "triggerPrice": float(leg1_trigger), "qty": int(leg1_qty)}
        }

    if st.button("Place GTT Order"):
        data = {
            "side": side,
            "symbol": symbol,
            "productType": product_type,
            "orderInfo": order_info
        }
        resp = fyres_post("/api/v3/gtt/orders/sync", data)
        st.write(resp)
        if resp.get("s") == "ok":
            st.success(f"GTT Order placed! Ref: {resp.get('id')}")
        else:
            st.error(f"GTT order failed: {resp.get('message')}")
