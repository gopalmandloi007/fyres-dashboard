import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
from fyres_utils import fetch_positions, squareoff_positions, fetch_holdings, sell_holding, fetch_orders
import time

def show():
    st.header("Square Off: Positions & Holdings")

    tab1, tab2 = st.tabs(["Positions", "Holdings"])

    with tab1:
        st.subheader("Square Off Positions")
        resp = fetch_positions()
        if resp.get("s") == "ok":
            positions = resp.get("netPositions", []) or resp.get("positions", [])
            if positions:
                df = pd.DataFrame(positions)
                id_list = [str(x) for x in df["id"].tolist()] if "id" in df.columns else []
                selected_ids = st.multiselect("Select Position IDs to Square Off", id_list)
                all_selected = st.checkbox("Square Off ALL Positions", value=(len(selected_ids)==0))
                if st.button("Square Off Positions"):
                    ids = None if all_selected else selected_ids
                    resp2 = squareoff_positions(ids)
                    st.write("API Response:", resp2)
                    if resp2.get("s") == "ok":
                        st.success(resp2.get("message", "Positions squared off!"))
                    else:
                        st.error(resp2.get("message", "Failed to square off."))
                st.dataframe(df)
            else:
                st.info("No open positions.")
        else:
            st.error("Could not fetch positions.")

    with tab2:
        st.subheader("Sell Holdings (Square Off)")
        resp = fetch_holdings()
        if resp.get("s") == "ok":
            holdings = resp.get("holdings", [])
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
                        qty_to_sell = st.number_input(
                            f"Qty to Sell for {row['symbol']}",
                            min_value=1,
                            max_value=int(row['quantity']),
                            value=int(row['quantity']),
                            key=f"qty_{row['symbol']}"
                        )
                        order_type = st.selectbox(
                            f"Order Type for {row['symbol']}",
                            [("Market", 2), ("Limit", 1)],
                            format_func=lambda x: x[0],
                            key=f"type_{row['symbol']}"
                        )
                        limit_price = None
                        if order_type[1] == 1:
                            limit_price = st.number_input(
                                f"Limit Price for {row['symbol']}",
                                value=float(row.get("ltp", 0)),
                                key=f"lp_{row['symbol']}"
                            )
                        if st.button(f"Sell {qty_to_sell} of {row['symbol']}", key=f"sell_{row['symbol']}"):
                            resp2 = sell_holding(row['symbol'], qty_to_sell, order_type[1], limit_price)
                            st.write("Order Sell Response:", resp2)
                            time.sleep(2)
                            orders = fetch_orders()
                            st.write("Order Book Snapshot:", orders)
                            if resp2.get("s") == "ok":
                                st.success(f"Sell Order Placed for {row['symbol']}")
                            else:
                                st.error(resp2.get("message", "Sell failed"))
                else:
                    st.info("Select holdings to sell from the dropdown above.")
                st.dataframe(df)
            else:
                st.info("No holdings found.")
        else:
            st.error("Could not fetch holdings.")

if __name__ == "__main__":
    show()
