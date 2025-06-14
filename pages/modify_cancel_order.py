import streamlit as st
from fyres_utils import fyres_patch, fyres_delete

def show():
    st.header("Modify/Cancel Normal Order")
    order_id = st.text_input("Order ID to Modify/Cancel")
    action = st.radio("Action", ["Modify", "Cancel"])

    if not order_id:
        st.info("Please enter an Order ID.")
        return

    if action == "Modify":
        qty = st.number_input("New Qty", min_value=1, step=1)
        limit_price = st.number_input("New Limit Price", value=0.0)
        stop_price = st.number_input("New Stop Price", value=0.0)
        order_type = st.selectbox(
            "Order Type",
            [("Limit", 1), ("Market", 2), ("Stop (SL-M)", 3), ("Stoplimit (SL-L)", 4)],
            format_func=lambda x: x[0]
        )[1]
        side = st.selectbox(
            "Side",
            [("Buy", 1), ("Sell", -1)],
            format_func=lambda x: x[0]
        )[1]
        if st.button("Modify Order"):
            data = {
                "id": order_id,
                "qty": int(qty),
                "type": order_type,
                "side": side,
                "limitPrice": float(limit_price),
                "stopPrice": float(stop_price)
            }
            resp = fyres_patch("/api/v3/orders/sync", data)
            st.write(resp)
            if resp.get("s") == "ok":
                st.success("Order modified!")
            else:
                st.error(f"Modify failed: {resp.get('message')}")
    else:
        if st.button("Cancel Order"):
            data = {"id": order_id}
            resp = fyres_delete("/api/v3/orders/sync", data)
            st.write(resp)
            if resp.get("s") == "ok":
                st.success("Order cancelled!")
            else:
                st.error(f"Cancel failed: {resp.get('message')}")
