import sys
import os
import re
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)

import streamlit as st
import pandas as pd

from fyres_utils import (
    fetch_positions, squareoff_positions,
    fetch_holdings, fetch_orders,
    place_single_order
)

def get_alphanumeric(text, default="OrderTag1"):
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned if cleaned else default

def fyers_sell_form(row, symbol, qty, unique_id):
    st.markdown("---")
    with st.form(f"sell_form_{unique_id}"):
        # 1. Quantity: Full/Partial radio, then qty input if Partial
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

        # 2. Order Type: Market/Limit radio, then price input if Limit
        order_type_tuple = st.radio(
            "Order Type",
            [("Market", 2), ("Limit", 1)],
            horizontal=True,
            key=f"ordertype_{unique_id}"
        )
        order_type = order_type_tuple[1]

        if order_type == 1:  # Limit order
            default_price = float(row.get("ltp") or row.get("avg_price") or row.get("buy_price") or 0.0)
            limit_price = st.number_input(
                "Limit Price (₹)",
                min_value=0.01,
                value=round(default_price, 2),
                key=f"price_{unique_id}"
            )
        else:
            limit_price = 0.0  # Market order: no price

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
                "type": order_type,
                "side": -1,
                "productType": "CNC",
                "limitPrice": float(limit_price) if order_type == 1 else 0,
                "stopPrice": 0,
                "validity": validity,
                "disclosedQty": int(disclosed_qty),
                "offlineOrder": offline_order,
                "orderTag": order_tag,
            }
            if order_type == 2:
                order_data["limitPrice"] = 0
                order_data["stopPrice"] = 0

            st.write("Order Data Being Sent:", order_data)
            try:
                st.write("Placing order...")
                resp = place_single_order(order_data)
                st.write("API Response:", resp)
                if resp.get("s") == "ok":
                    st.success(f"Order Placed! Ref: {resp.get('id', '')}")
                else:
                    st.error(f"Order Failed: {resp.get('message', '')}")
            except Exception as e:
                st.error(f"Exception: {e}")

def show():
    st.header("⚡ Fyers Dashboard: Square Off Positions & Holdings")
    st.subheader("Sell Holdings (Row-wise, Like Definedge)")
    st.markdown("---")

    # --- Holdings Table ---
    resp = fetch_holdings()
    if resp.get("s") == "ok":
        holdings = resp.get("holdings", [])
        if holdings:
            df = pd.DataFrame(holdings)
            st.markdown("#### Holdings List")
            columns = st.columns([1.7, 1.3, 1.2, 1.2, 1.3, 1.2])
            labels = ["Symbol", "Qty", "LTP", "P&L", "Buy Price", "Sell"]
            for i, label in enumerate(labels):
                columns[i].markdown(f"**{label}**")
            sell_id = st.session_state.get("sell_id", None)
            for idx, row in df.iterrows():
                symbol = row.get("symbol", f"sym_{idx}")
                qty = int(row.get("quantity", 0))
                ltp = row.get("ltp", 0)
                pnl = row.get("pl", 0)
                buy_price = row.get("avg_price", row.get("buy_price", 0))
                columns = st.columns([1.7, 1.3, 1.2, 1.2, 1.3, 1.2])
                columns[0].write(symbol)
                columns[1].write(qty)
                columns[2].write(ltp)
                columns[3].write(pnl)
                columns[4].write(buy_price)
                if columns[5].button("Sell", key=f"sell_btn_{symbol}"):
                    st.session_state["sell_id"] = f"HOLD_{idx}"
                    st.rerun()
                if sell_id == f"HOLD_{idx}":
                    fyers_sell_form(row, symbol, qty, f"HOLD_{idx}")
    else:
        st.error("Could not fetch holdings.")

    st.markdown("---")
    st.subheader("📝 Square Off Positions (simple, use Fyers squareoff API)")
    # --- Positions Table (simple, like above) ---
    resp = fetch_positions()
    if resp.get("s") == "ok":
        positions = resp.get("netPositions", []) or resp.get("positions", [])
        if positions:
            df = pd.DataFrame(positions)
            st.markdown("#### Positions List")
            columns = st.columns([1.7, 1.3, 1.2, 1.2, 1.3, 1.2])
            labels = ["Symbol", "Qty", "P&L", "Type", "ID", "Square Off"]
            for i, label in enumerate(labels):
                columns[i].markdown(f"**{label}**")
            sq_id = st.session_state.get("sq_id", None)
            for idx, row in df.iterrows():
                symbol = row.get("symbol", f"sym_{idx}")
                qty = int(row.get("netQty", row.get("quantity", 0)))
                pnl = row.get("pl", 0)
                product_type = row.get("productType", row.get("product_type", ""))
                pos_id = row.get("id", f"pos_{idx}")
                columns = st.columns([1.7, 1.3, 1.2, 1.2, 1.3, 1.2])
                columns[0].write(symbol)
                columns[1].write(qty)
                columns[2].write(pnl)
                columns[3].write(product_type)
                columns[4].write(pos_id)
                if columns[5].button("Square Off", key=f"squareoff_btn_{pos_id}"):
                    st.session_state["sq_id"] = f"POS_{idx}"
                    st.rerun()
                if sq_id == f"POS_{idx}":
                    with st.form(f"squareoff_form_{pos_id}"):
                        st.markdown(f"**Are you sure to Square Off this position?**")
                        submitted = st.form_submit_button("🟢 Confirm Square Off")
                        if submitted:
                            with st.spinner("Placing square off..."):
                                try:
                                    resp2 = squareoff_positions([pos_id])
                                    st.write("API Response:", resp2)
                                    if resp2.get("s", "") == "ok":
                                        st.success("Position Squared Off!")
                                    else:
                                        st.error(resp2.get("message", "Failed to square off"))
                                except Exception as e:
                                    st.error(f"Exception: {e}")
                            st.session_state["sq_id"] = None
                            st.rerun()
    else:
        st.error("Could not fetch positions.")

if __name__ == "__main__":
    show()
