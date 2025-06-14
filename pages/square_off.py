import streamlit as st
import re
from fyres_utils import fetch_holdings, place_single_order

def get_alphanumeric(text, default="tag1"):
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned if cleaned else default

def squareoff_form(item, qty, symbol, idx, active_form_idx):
    unique_id = f"squareoff_{idx}"
    if active_form_idx != idx:
        return

    form_state_key = f"{unique_id}_order_state"
    if form_state_key not in st.session_state:
        st.session_state[form_state_key] = None

    with st.form(key=f"{unique_id}_form", clear_on_submit=True):
        qty_option = st.radio(
            "Quantity to Square Off",
            ["Full", "Partial"],
            horizontal=True,
            key=f"{unique_id}_qtyopt"
        )
        if qty_option == "Partial":
            squareoff_qty = st.number_input(
                "Enter quantity to square off",
                min_value=1,
                max_value=int(qty),
                value=1,
                key=f"{unique_id}_squareoffqty"
            )
        else:
            squareoff_qty = int(qty)

        order_type = st.radio(
            "Order Type",
            ["Market Order", "Limit Order"],
            horizontal=True,
            key=f"{unique_id}_ordertype"
        )
        if order_type == "Limit Order":
            default_price = float(
                item.get("ltp") or item.get("avg_price") or item.get("buy_price") or 0
            )
            squareoff_price = st.number_input(
                "Limit Price (₹)",
                min_value=0.01,
                value=round(default_price, 2) if default_price > 0 else 0.01,
                key=f"{unique_id}_price"
            )
            fyers_order_type = 1
        else:
            squareoff_price = 0.0
            fyers_order_type = 2

        validity = st.selectbox(
            "Order Validity", ["DAY", "IOC"], index=0, key=f"{unique_id}_validity"
        )
        remarks = st.text_input(
            "Order Tag (optional)",
            max_chars=15,
            key=f"{unique_id}_remarks"
        )

        disclose = st.checkbox(
            "Disclose Partial Quantity?", key=f"{unique_id}_disclose"
        )
        if disclose:
            disclosed_quantity = st.number_input(
                "Disclosed Quantity",
                min_value=1,
                max_value=int(squareoff_qty),
                value=int(squareoff_qty),
                key=f"{unique_id}_discloseqty"
            )
        else:
            disclosed_quantity = 0

        submitted = st.form_submit_button("🟢 Place Sell Order")

        # Prepare the order_data in advance for confirmation
        order_data = {
            "symbol": symbol,
            "qty": int(squareoff_qty),
            "type": fyers_order_type,
            "side": -1,
            "productType": "CNC",
            "limitPrice": float(squareoff_price) if fyers_order_type == 1 else 0,
            "stopPrice": 0,
            "validity": validity,
            "disclosedQty": int(disclosed_quantity),
            "offlineOrder": False,
            "orderTag": get_alphanumeric(remarks, default=f"Sell{symbol.replace('-','').replace(':','')}")
        }

        if submitted:
            if squareoff_qty > qty:
                st.error("Cannot square off more than available quantity!")
                return
            # Store the pending order in session state for confirmation
            st.session_state[form_state_key] = order_data

    # If order is pending confirmation, show a modal dialog
    if st.session_state[form_state_key]:
        with st.modal("Confirm Sell Order"):
            st.write("**Please confirm your order before final placement:**")
            st.json(st.session_state[form_state_key])
            col1, col2 = st.columns(2)
            confirm = col1.button("✅ Confirm Order", key=f"{unique_id}_confirm")
            cancel = col2.button("❌ Cancel", key=f"{unique_id}_cancel")
            if confirm:
                with st.spinner("Placing order..."):
                    resp = place_single_order(st.session_state[form_state_key])
                if resp.get("s") == "ok":
                    st.success(f"Order Placed! Ref: {resp.get('id', '')}")
                else:
                    st.error(f"Order Failed: {resp.get('message', '')}")
                st.session_state["active_sqoff_idx"] = None
                st.session_state[form_state_key] = None
                st.rerun()
            if cancel:
                st.session_state[form_state_key] = None
                st.rerun()

def show():
    st.title("⚡ Fyers CNC Square Off (Definedge Style)")
    st.markdown("---")
    resp = fetch_holdings()
    holdings = resp.get("holdings", [])
    if not holdings:
        st.info("No holdings to square off.")
        return

    st.markdown("#### Your Holdings")
    columns = st.columns([2, 1, 1, 1, 1])
    for i, label in enumerate(["Symbol", "Qty", "LTP", "Avg Price", "Square Off"]):
        columns[i].markdown(f"**{label}**")

    active_form_idx = st.session_state.get("active_sqoff_idx", None)

    for idx, h in enumerate(holdings):
        symbol = h.get("symbol", "")
        qty = int(h.get("quantity", 0))
        ltp = h.get("ltp", 0)
        avg_price = h.get("avg_price", 0)
        columns = st.columns([2, 1, 1, 1, 1])
        columns[0].write(symbol)
        columns[1].write(qty)
        columns[2].write(ltp)
        columns[3].write(avg_price)
        if columns[4].button("Square Off", key=f"sqoff_btn_{idx}"):
            st.session_state["active_sqoff_idx"] = idx
            st.rerun()
        squareoff_form(h, qty, symbol, idx, active_form_idx)

if __name__ == "__main__":
    show()
