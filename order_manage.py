import streamlit as st
from utils import get_fyers_client

def show():
    st.header("Cancel/Modify Orders (FYERS)")
    fyers = get_fyers_client()
    orders = fyers.orderbook()
    if orders.get('code') == 200:
        orders_data = orders.get('orderBook', [])
        pending_orders = [o for o in orders_data if int(o.get('status', 0)) in [1, 6] and int(o.get("remainingQuantity", 0)) > 0]
        if pending_orders:
            selection = st.selectbox("Select Pending Order", options=pending_orders, format_func=lambda o: f"{o['symbol']} [{o['id']}]")
            if st.button("Cancel Order"):
                resp = fyers.cancel_order({"id": selection['id']})
                st.write(resp)
            if st.button("Modify Order (change quantity)"):
                new_qty = st.number_input("New Qty", min_value=1, value=int(selection['qty']))
                resp = fyers.modify_order({
                    "id": selection['id'],
                    "type": selection['type'],
                    "qty": int(new_qty),
                    "limitPrice": selection['limitPrice'],
                    "stopPrice": selection['stopPrice'],
                    "disclosedQty": max(1, int(new_qty * 0.1))
                })
                st.write(resp)
        else:
            st.info("No pending orders available.")
    else:
        st.error(f"Error fetching orders: {orders.get('message', 'No message available')}")
