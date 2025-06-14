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
    st.header("Square Off: Positions & Holdings (Fyers Row-wise Action)")

    tab1, tab2 = st.tabs(["Positions", "Holdings"])

    # --- POSITIONS TAB ---
    with tab1:
        st.subheader("Square Off Positions (Row-wise)")
        resp = fetch_positions()
        if resp.get("s") == "ok":
            positions = resp.get("netPositions", []) or resp.get("positions", [])
            if positions:
                df = pd.DataFrame(positions)
                st.write("**Open Positions:**")
                for idx, row in df.iterrows():
                    pos_id = str(row.get("id", f"pos_{idx}"))
                    with st.expander(f"{row.get('symbol', '')} | Qty: {row.get('netQty', '')} | P&L: {row.get('pl', '')}"):
                        st.write(row)
                        if st.button("Square Off", key=f"pos_squareoff_btn_{pos_id}"):
                            st.session_state[f"show_pos_mod_{pos_id}"] = True
                        if st.session_state.get(f"show_pos_mod_{pos_id}", False):
                            st.markdown("**Modify Square Off (You can just confirm below):**")
                            st.write(f"Position ID: {pos_id}")
                            # Most brokers just need ID to squareoff, but you can add qty etc. if your API supports
                            if st.button("Confirm & Place Square Off Order", key=f"place_pos_sq_{pos_id}"):
                                resp2 = squareoff_positions([pos_id])
                                st.write("API Response:", resp2)
                                if resp2.get("s", "") == "ok":
                                    st.success("Position Squared Off!")
                                    st.session_state[f"show_pos_mod_{pos_id}"] = False
                                else:
                                    st.error(resp2.get("message", "Failed to square off."))
                            if st.button("Cancel", key=f"cancel_pos_sq_{pos_id}"):
                                st.session_state[f"show_pos_mod_{pos_id}"] = False
            else:
                st.info("No open positions.")
        else:
            st.error("Could not fetch positions.")

    # --- HOLDINGS TAB ---
    with tab2:
        st.subheader("Sell Holdings (Row-wise)")
        resp = fetch_holdings()
        if resp.get("s") == "ok":
            holdings = resp.get("holdings", [])
            if holdings:
                df = pd.DataFrame(holdings)
                st.write("**Your Holdings:**")
                for idx, row in df.iterrows():
                    symbol = row.get("symbol", f"sym_{idx}")
                    with st.expander(f"{row.get('symbol', '')} | Qty: {row.get('quantity', '')} | P&L: {row.get('pl', '')}"):
                        st.write(row)
                        if st.button("Sell", key=f"hold_sell_btn_{symbol}"):
                            st.session_state[f"show_hold_mod_{symbol}"] = True
                        if st.session_state.get(f"show_hold_mod_{symbol}", False):
                            st.markdown("**Sell Order Details:**")
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
                            if st.button("Place Sell Order", key=f"place_hold_sell_{symbol}"):
                                resp2 = sell_holding(symbol, qty_to_sell, order_type[1], limit_price)
                                st.write("Order Sell Response:", resp2)
                                time.sleep(2)
                                orders = fetch_orders()
                                st.write("Order Book Snapshot:", orders)
                                if resp2.get("s", "") == "ok":
                                    st.success("Sell Order Placed!")
                                    st.session_state[f"show_hold_mod_{symbol}"] = False
                                else:
                                    st.error(resp2.get("message", "Sell failed"))
                            if st.button("Cancel", key=f"cancel_hold_sell_{symbol}"):
                                st.session_state[f"show_hold_mod_{symbol}"] = False
            else:
                st.info("No holdings found.")
        else:
            st.error("Could not fetch holdings.")

if __name__ == "__main__":
    show()
