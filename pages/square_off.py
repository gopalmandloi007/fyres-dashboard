import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import time

from fyres_utils import (
    fetch_positions, squareoff_positions,
    fetch_holdings, fetch_orders,
    place_single_order # <-- use this for actual order placing
)

def show():
    st.header("Square Off: Positions & Holdings (Row Action, Real Order)")

    tab1, tab2 = st.tabs(["Positions", "Holdings"])

    # Positions Tab (Row-wise)
    with tab1:
        st.subheader("Square Off Positions (Row)")
        resp = fetch_positions()
        if resp.get("s") == "ok":
            positions = resp.get("netPositions", []) or resp.get("positions", [])
            if positions:
                df = pd.DataFrame(positions)
                for idx, row in df.iterrows():
                    pos_id = str(row.get("id", f"pos_{idx}"))
                    symbol = row.get("symbol", "")
                    with st.expander(f"{symbol} | Qty: {row.get('netQty', row.get('quantity',''))} | P&L: {row.get('pl', '')}", expanded=False):
                        st.write(row)
                        # If you want to square off via order (not API), you could add similar order form here
                        # Otherwise, keep using squareoff_positions if that's correct for Fyers positions
                        if st.button("Square Off", key=f"squareoff_btn_{pos_id}"):
                            resp2 = squareoff_positions([pos_id])
                            st.write("API Response:", resp2)
                            if resp2.get("s", "") == "ok":
                                st.success("Position Squared Off!")
                            else:
                                st.error(resp2.get("message", "Failed to square off"))
                            time.sleep(1.5)
            else:
                st.info("No open positions.")
        else:
            st.error("Could not fetch positions.")

    # Holdings Tab (Row-wise, with real order form)
    with tab2:
        st.subheader("Sell Holdings (Row, Real Order)")
        resp = fetch_holdings()
        if resp.get("s") == "ok":
            holdings = resp.get("holdings", [])
            if holdings:
                df = pd.DataFrame(holdings)
                for idx, row in df.iterrows():
                    symbol = row.get("symbol", f"sym_{idx}")
                    ltp = float(row.get("ltp", 0))
                    with st.expander(f"{symbol} | Qty: {row.get('quantity','')}", expanded=False):
                        st.write(row)
                        if st.button("Sell", key=f"sell_btn_{symbol}"):
                            st.session_state[f"show_mod_{symbol}"] = True

                        if st.session_state.get(f"show_mod_{symbol}", False):
                            st.markdown("**Modify Sell Order:**")
                            qty_to_sell = st.number_input(
                                "Quantity to Sell",
                                min_value=1,
                                max_value=int(row.get("quantity", 1)),
                                value=int(row.get("quantity", 1)),
                                key=f"qty_{symbol}"
                            )
                            order_type = st.radio(
                                "Order Type",
                                [("Market", 2), ("Limit", 1)],
                                format_func=lambda x: x[0],
                                horizontal=True,
                                key=f"type_{symbol}"
                            )
                            limit_price = ltp
                            if order_type[1] == 1:
                                limit_price = st.number_input(
                                    "Limit Price",
                                    value=ltp,
                                    key=f"lp_{symbol}"
                                )
                            validity = st.selectbox("Validity", ["DAY", "IOC"], key=f"validity_{symbol}")
                            disclosed_qty = st.number_input("Disclosed Qty", value=0, step=1, min_value=0, key=f"dq_{symbol}")
                            offline_order = st.checkbox("Offline Order", value=False, key=f"offline_{symbol}")
                            order_tag = st.text_input("Order Tag", value=f"sell_{symbol}", key=f"tag_{symbol}")

                            if st.button("Place Sell Order", key=f"place_sell_{symbol}"):
                                order_data = {
                                    "symbol": symbol,
                                    "qty": int(qty_to_sell),
                                    "type": order_type[1],
                                    "side": -1,  # SELL
                                    "productType": "CNC",
                                    "limitPrice": float(limit_price) if order_type[1] == 1 else 0,
                                    "stopPrice": 0,
                                    "validity": validity,
                                    "disclosedQty": int(disclosed_qty),
                                    "offlineOrder": offline_order,
                                    "orderTag": order_tag.strip() if order_tag.strip() else f"tag_{symbol}"
                                }
                                # For market, clear limit/stop price
                                if order_type[1] == 2:
                                    order_data["limitPrice"] = 0
                                    order_data["stopPrice"] = 0

                                st.write("Order Review:", order_data)
                                try:
                                    resp2 = place_single_order(order_data)
                                    st.write("Order Sell Response:", resp2)
                                    if resp2.get("s", "") == "ok":
                                        st.success(f"Sell Order Placed! Ref: {resp2.get('id','')}")
                                    else:
                                        st.error(resp2.get("message", "Sell failed"))
                                    st.session_state[f"show_mod_{symbol}"] = False
                                    time.sleep(1.5)
                                except Exception as e:
                                    st.error(f"Exception: {e}")
                            if st.button("Cancel", key=f"cancel_{symbol}"):
                                st.session_state[f"show_mod_{symbol}"] = False
            else:
                st.info("No holdings found.")
        else:
            st.error("Could not fetch holdings.")

if __name__ == "__main__":
    show()
