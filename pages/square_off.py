import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import time

# Import your actual Definedge utils (replace with your own API calls as needed)
from definedge_utils import (
    fetch_positions,         # Should return a list of positions, with 'position_id' and other details
    squareoff_positions,     # Should accept a list of position_ids or None for ALL
    fetch_holdings,          # Should return a list of holdings, with 'symbol', 'quantity', 'ltp', etc.
    place_sell_order,        # Should accept symbol, qty, order_type, limit_price (if limit), etc.
    fetch_orders             # Should return latest orders
)

def show():
    st.header("Square Off: Positions & Holdings (Definedge)")

    tab1, tab2 = st.tabs(["Positions", "Holdings"])

    # --- Positions Tab ---
    with tab1:
        st.subheader("Square Off Positions")
        positions = fetch_positions()
        if positions:
            df = pd.DataFrame(positions)
            id_list = [str(x) for x in df["position_id"].tolist()] if "position_id" in df.columns else []
            selected_ids = st.multiselect("Select Position IDs to Square Off", id_list)
            all_selected = st.checkbox("Square Off ALL Positions", value=(len(selected_ids) == 0))
            if st.button("Square Off Positions"):
                ids = None if all_selected else selected_ids
                resp2 = squareoff_positions(ids)
                st.write("API Response:", resp2)
                if resp2.get("status", "") == "ok":
                    st.success(resp2.get("message", "Positions squared off!"))
                else:
                    st.error(resp2.get("message", "Failed to square off."))
            st.dataframe(df)
        else:
            st.info("No open positions found.")

    # --- Holdings Tab ---
    with tab2:
        st.subheader("Sell Holdings (Partial/Market/Limit)")
        holdings = fetch_holdings()
        if holdings:
            df = pd.DataFrame(holdings)
            symbol_list = [str(x) for x in df["symbol"].tolist()] if "symbol" in df.columns else []
            selected_symbols = st.multiselect("Select Holdings to Sell", symbol_list)
            if selected_symbols:
                for symbol in selected_symbols:
                    sel_row = df[df["symbol"] == symbol]
                    if sel_row.empty:
                        continue
                    row = sel_row.iloc[0]
                    st.markdown(f"**{row['symbol']}** | Qty held: {row['quantity']}")
                    qty_key = f"qty_{row['symbol']}"
                    order_type_key = f"type_{row['symbol']}"
                    limit_price_key = f"lp_{row['symbol']}"
                    sell_btn_key = f"sell_{row['symbol']}_{st.session_state.get(order_type_key, 2)}"

                    qty_to_sell = st.number_input(
                        f"Qty to Sell for {row['symbol']}",
                        min_value=1,
                        max_value=int(row['quantity']),
                        value=int(row['quantity']),
                        key=qty_key
                    )
                    order_type = st.selectbox(
                        f"Order Type for {row['symbol']}",
                        [("Market", "MARKET"), ("Limit", "LIMIT")],
                        format_func=lambda x: x[0],
                        key=order_type_key
                    )
                    limit_price = None
                    if order_type[1] == "LIMIT":
                        limit_price = st.number_input(
                            f"Limit Price for {row['symbol']}",
                            value=float(row.get("ltp", 0)),
                            key=limit_price_key
                        )
                    if st.button(f"Sell {qty_to_sell} of {row['symbol']}", key=sell_btn_key):
                        resp2 = place_sell_order(
                            symbol=row['symbol'],
                            qty=qty_to_sell,
                            order_type=order_type[1],
                            limit_price=limit_price
                        )
                        st.write("Order Sell Response:", resp2)
                        time.sleep(2)
                        orders = fetch_orders()
                        st.write("Order Book Snapshot:", orders)
                        if resp2.get("status", "") == "ok":
                            st.success(f"Sell Order Placed for {row['symbol']}")
                        else:
                            st.error(resp2.get("message", "Sell failed"))
            else:
                st.info("Select holdings to sell from the dropdown above.")
            st.dataframe(df)
        else:
            st.info("No holdings found.")

if __name__ == "__main__":
    show()
