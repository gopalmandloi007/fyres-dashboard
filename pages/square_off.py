import streamlit as st
import re

def get_alphanumeric(text, default="OrderTag1"):
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned if cleaned else default

def fyers_squareoff_form(item, qty, symbol, place_single_order):
    unique_id = f"Fyers_{symbol}"

    with st.form(f"fyers_sqoff_form_{unique_id}"):
        # Full/Partial
        qty_option = st.radio(
            "Quantity to Sell",
            ["Full", "Partial"],
            horizontal=True,
            key=f"qtyopt_{unique_id}"
        )
        if qty_option == "Partial":
            sell_qty = st.number_input(
                "Enter quantity to sell",
                min_value=1,
                max_value=int(qty),
                value=1,
                key=f"sellqty_{unique_id}"
            )
        else:
            sell_qty = int(qty)

        # Market/Limit
        order_type = st.radio(
            "Order Type",
            ["Market", "Limit"],
            horizontal=True,
            key=f"ordertype_{unique_id}"
        )
        if order_type == "Limit":
            default_price = float(item.get("ltp") or item.get("avg_price") or item.get("buy_price") or 0.0)
            limit_price = st.number_input(
                "Limit Price (₹)",
                min_value=0.01,
                value=round(default_price, 2),
                key=f"price_{unique_id}"
            )
            fyers_order_type = 1
        else:
            limit_price = 0.0
            fyers_order_type = 2

        validity = st.selectbox(
            "Order Validity",
            ["DAY", "IOC"],
            index=0,
            key=f"validity_{unique_id}"
        )

        disclosed_qty = st.number_input(
            "Disclosed Quantity (optional)",
            min_value=0,
            max_value=int(sell_qty),
            value=0,
            key=f"discloseqty_{unique_id}"
        )
        offline_order = st.checkbox(
            "Offline Order",
            value=False,
            key=f"offline_{unique_id}"
        )
        order_tag_raw = st.text_input(
            "Order Tag (optional, only letters/numbers allowed!)",
            value=f"sell{symbol.replace('-','').replace(':','')}",
            key=f"tag_{unique_id}"
        )
        order_tag = get_alphanumeric(order_tag_raw, default=f"Sell{symbol.replace('-','').replace(':','')}")

        submitted = st.form_submit_button("🟢 Place Sell Order")

        if submitted:
            order_data = {
                "symbol": symbol,
                "qty": int(sell_qty),
                "type": fyers_order_type,
                "side": -1,
                "productType": "CNC",
                "limitPrice": float(limit_price) if fyers_order_type == 1 else 0,
                "stopPrice": 0,
                "validity": validity,
                "disclosedQty": int(disclosed_qty),
                "offlineOrder": offline_order,
                "orderTag": order_tag,
            }
            st.write("Order Data Being Sent:", order_data)
            with st.spinner("Placing order..."):
                resp = place_single_order(order_data)
            status = resp.get('s') or resp.get('message') or resp
            if resp.get("s") != "ok":
                st.error(f"Order Failed: {resp.get('message','Error')}")
            else:
                st.success(f"Order Placed! Ref: {resp.get('id', '')}")
            st.rerun()
