import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import time

from fyres_utils import (
    fetch_positions, squareoff_positions,
    fetch_holdings, sell_holding, fetch_orders
)

def show():
    st.header("Square Off: Positions & Holdings (Row Action)")

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
                    exp_key = f"expander_pos_{pos_id}"
                    show_mod_key = f"show_mod_pos_{pos_id}"

                    with st.expander(f"{row.get('symbol','')} | Qty: {row.get('netQty', row.get('quantity',''))} | P&L: {row.get('pl', '')}", expanded=False):
                        st.write(row)
                        if st.button("Square Off", key=f"squareoff_btn_{pos_id}"):
                            st.session_state[show_mod_key] = True

                        if st.session_state.get(show_mod_key, False):
                            st.markdown("**Are you sure to Square Off this position?**")
                            if st.button("Confirm Square Off", key=f"confirm_sq_{pos_id}"):
                                resp2 = squareoff_positions([pos_id])
                                st.write("API Response:", resp2)
                                if resp2.get("s", "") == "ok":
                                    st.success("Position Squared Off!")
                                else:
                                    st.error(resp2.get("message", "Failed to square off"))
                                st.session_state[show_mod_key] = False
                                time.sleep(1.5)
                            if st.button("Cancel", key=f"cancel_sq_{pos_id}"):
                                st.session_state[show_mod_key] = False
            else:
                st.info("No open positions.")
        else:
            st.error("Could not fetch positions.")

    # Holdings Tab (Row-wise)
    with tab2:
        st.subheader("Sell Holdings (Row)")
        resp = fetch_holdings()
        if resp.get("s") == "ok":
            holdings = resp.get("holdings", [])
            if holdings:
                df = pd.DataFrame(holdings)
                for idx, row in df.iterrows():
                    symbol = row.get("symbol", f"sym_{idx}")
                    exp_key = f"expander_hold_{symbol}"
                    show_mod_key = f"show_mod_hold_{symbol}"

                    with st.expander(f"{row.get('symbol','')} | Qty: {row.get('quantity','')}", expanded=False):
                        st.write(row)
                        if st.button("Sell", key=f"sell_btn_{symbol}"):
                            st.session_state[show_mod_key] = True

                        if st.session_state.get(show_mod_key, False):
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
                            limit_price = None
                            if order_type[1] == 1:
                                limit_price = st.number_input(
                                    "Limit Price",
                                    value=float(row.get("ltp", 0)),
                                    key=f"lp_{symbol}"
                                )
                            if st.button("Place Sell Order", key=f"place_sell_{symbol}"):
                                try:
                                    resp2 = sell_holding(symbol, qty_to_sell, order_type[1], limit_price)
                                    st.write("Order Sell Response:", resp2)
                                    if resp2.get("s", "") == "ok":
                                        st.success("Sell Order Placed!")
                                    else:
                                        st.error(resp2.get("message", "Sell failed"))
                                    st.session_state[show_mod_key] = False
                                    time.sleep(1.5)
                                except Exception as e:
                                    st.error(f"Exception: {e}")
                            if st.button("Cancel", key=f"cancel_{symbol}"):
                                st.session_state[show_mod_key] = False
            else:
                st.info("No holdings found.")
        else:
            st.error("Could not fetch holdings.")

if __name__ == "__main__":
    show()
