import streamlit as st
import re
from fyres_utils import fetch_holdings, fetch_positions, place_single_order

def get_alphanumeric(text, default="OrderTag1"):
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned if cleaned else default

def squareoff_form_fyers(item, qty, symbol, is_position=False):
    label = "Position" if is_position else "Holding"
    unique_id = f"{label}_{symbol}"

    with st.form(f"fyres_squareoff_form_{unique_id}"):
        qty_option = st.radio(
            f"Quantity to Sell for {symbol}",
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

        order_type = st.radio(
            "Order Type",
            ["Market Order", "Limit Order"],
            horizontal=True,
            key=f"ordertype_{unique_id}"
        )
        if order_type == "Limit Order":
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
            st.session_state["fy_sq_id"] = None
            st.rerun()

def show():
    st.title("⚡ Fyers Dashboard")
    st.subheader("💼 Square Off Holdings & Positions")
    st.markdown("---")

    # --- Holdings Table ---
    st.header("📦 Holdings")
    resp = fetch_holdings()
    holdings = resp.get("holdings", [])
    hold_cols = ["symbol", "quantity", "ltp", "avg_price"]
    col_labels = ["Symbol", "Qty", "LTP", "Avg Price"]
    st.markdown("#### Holdings List")
    columns = st.columns([1.5, 1.2, 1.2, 1.3, 1.2])
    for i, label in enumerate(col_labels):
        columns[i].markdown(f"**{label}**")
    columns[-1].markdown("**Sell**")

    user_holdings = []
    for h in holdings:
        qty = int(h.get("quantity", 0))
        symbol = h.get("symbol", "")
        if qty > 0 and symbol:
            user_holdings.append((h, qty, symbol))
    if not user_holdings:
        st.info("No holdings to sell.")
    else:
        fy_sq_id = st.session_state.get("fy_sq_id", None)
        for idx, (holding, qty, symbol) in enumerate(user_holdings):
            columns = st.columns([1.5, 1.2, 1.2, 1.3, 1.2])
            for i, key in enumerate(hold_cols):
                columns[i].write(holding.get(key, ""))
            if columns[-1].button("Sell", key=f"sell_btn_{symbol}"):
                st.session_state["fy_sq_id"] = f"HOLD_{idx}"
                st.rerun()
            if fy_sq_id == f"HOLD_{idx}":
                squareoff_form_fyers(holding, qty, symbol, is_position=False)

    # --- Positions Table ---
    st.header("📝 Positions")
    resp = fetch_positions()
    positions = resp.get("netPositions", []) or resp.get("positions", [])
    pos_cols = ["symbol", "netQty", "avg_price", "pl"]
    pos_labels = ["Symbol", "Net Qty", "Avg Price", "P&L"]
    st.markdown("#### Positions List")
    columns = st.columns([1.5, 1.2, 1.3, 1.2, 1.2])
    for i, label in enumerate(pos_labels):
        columns[i].markdown(f"**{label}**")
    columns[-1].markdown("**Square Off**")

    user_positions = []
    for p in positions:
        qty = int(p.get("netQty", p.get("quantity", 0)))
        symbol = p.get("symbol", "")
        if qty != 0 and symbol:
            user_positions.append((p, qty, symbol))
    if not user_positions:
        st.info("No open positions to square off.")
    else:
        fy_pos_id = st.session_state.get("fy_pos_id", None)
        for idx, (pos, qty, symbol) in enumerate(user_positions):
            columns = st.columns([1.5, 1.2, 1.3, 1.2, 1.2])
            for i, key in enumerate(pos_cols):
                columns[i].write(pos.get(key, ""))
            if columns[-1].button("Square Off", key=f"sqoff_btn_{symbol}_{idx}"):
                st.session_state["fy_pos_id"] = f"POS_{idx}"
                st.rerun()
            if fy_pos_id == f"POS_{idx}":
                squareoff_form_fyers(pos, qty, symbol, is_position=True)

if __name__ == "__main__":
    show()
