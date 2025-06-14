import streamlit as st
from fyres_utils import modify_gtt_order, cancel_gtt_order

def show():
    st.header("Modify/Cancel GTT Order")

    order_id = st.text_input("Order ID to modify/cancel")

    with st.expander("Modify GTT Order"):
        price1 = st.number_input("New Leg 1 Price", value=100.0)
        trigger_price1 = st.number_input("New Leg 1 Trigger Price", value=100.0)
        qty1 = st.number_input("New Leg 1 Qty", value=1, min_value=1, step=1)
        oco = st.checkbox("OCO Modify?", value=False)
        price2 = trigger_price2 = qty2 = None
        if oco:
            price2 = st.number_input("New Leg 2 Price", value=90.0)
            trigger_price2 = st.number_input("New Leg 2 Trigger Price", value=90.0)
            qty2 = st.number_input("New Leg 2 Qty", value=1, min_value=1, step=1)
        if st.button("Modify GTT Order"):
            order_info = {
                "leg1": {
                    "price": price1,
                    "triggerPrice": trigger_price1,
                    "qty": int(qty1)
                }
            }
            if oco:
                order_info["leg2"] = {
                    "price": price2,
                    "triggerPrice": trigger_price2,
                    "qty": int(qty2)
                }
            resp = modify_gtt_order(order_id, order_info)
            st.write("API Response:", resp)
            if resp.get("s") == "ok":
                st.success(f"Order modified! ID: {resp.get('id')}")
            else:
                st.error(f"Error: {resp.get('message')}")

    with st.expander("Cancel GTT Order"):
        if st.button("Cancel GTT Order"):
            resp = cancel_gtt_order(order_id)
            st.write("API Response:", resp)
            if resp.get("s") == "ok":
                st.success(f"Order cancelled! ID: {resp.get('id')}")
            else:
                st.error(f"Error: {resp.get('message')}")

if __name__ == "__main__":
    show()
