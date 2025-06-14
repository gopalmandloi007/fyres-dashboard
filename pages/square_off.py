import streamlit as st
import re
from fyres_utils import fetch_holdings, place_single_order

def get_alphanumeric(text, default="tag1"):
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned if cleaned else default

def squareoff_form(item, qty, symbol, idx):
    unique_id = f"squareoff_{symbol}_{idx}"
    with st.form(key=f"{unique_id}_form"):
        # Full/Partial selection
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

        # Market/Limit selection
        order_type = st.radio(
            "Order Type",
            ["Market Order", "Limit Order"],
            horizontal=True,
            key=f"{unique_id}_ordertype"
        )
        if order_type == "Limit Order":
            default_price = float(item.get("ltp") or item.get("avg_price") or item.get("buy_price") or 0)
            squareoff_price = st.number_input(
                "Limit Price (₹)", min_value=0.01, value=round(default_price, 2), key=f"{unique_id}_price"
            )
            fyers_order_type = 1
        else:
            squareoff_price = 0.0
            fyers_order_type = 2

        validity = st.selectbox("Order Validity", ["DAY", "IOC"], index=0, key=f"{unique_id}_validity")
        remarks = st.text_input("Order Tag (optional)", key=f"{unique_id}_remarks")

        disclose = st.checkbox("Disclose Partial Quantity?", key=f"{unique_id}_disclose")
        if disclose:
            disclosed_quantity = st.number_input(
                "Disclosed Quantity", min_value=1, max_value=int(squareoff_qty), value=1, key=f"{unique_id}_discloseqty"
            )
        else:
            disclosed_quantity = 0

        submitted = st.form_submit_button("🟢 Place Sell Order")
        if submitted:
            order_data = {
                "symbol": symbol,
                "qty": int(squareoff_qty),
                "type": fyers_order_type,
                "side": -1,  # Sell
                "productType": "CNC",
                "limitPrice": float(squareoff_price) if fyers_order_type == 1 else 0,
                "stopPrice": 0,
                "validity": validity,
                "disclosedQty": int(disclosed_quantity),
                "offlineOrder": False,
                "orderTag": get_alphanumeric(remarks, default=f"Sell{symbol.replace('-','').replace(':','')}")
            }
            st.write("Order Data Being Sent:", order_data)
            with st.spinner("Placing order..."):
                resp = place_single_order(order_data)
            if resp.get("s") == "ok":
                st.success(f"Order Placed! Ref: {resp.get('id', '')}")
            else:
                st.error(f"Order Failed: {resp.get('message', '')}")
            st.session_state["active_sqoff_idx"] = None
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
    show_idx = st.session_state.get("active_sqoff_idx", None)

    for idx, h in enumerate(holdings):
        symbol = h.get("symbol", "")
        qty = int(h.get("quantity", 0))
        ltp = h.get("ltp", 0)
        avg_price = h.get("avg_price", 0)
        # Show table row
        cols = st.columns([2, 1, 1, 1, 1])
        cols[0].write(symbol)
        cols[1].write(qty)
        cols[2].write(ltp)
        cols[3].write(avg_price)
        if cols[4].button("Square Off", key=f"sqoff_btn_{symbol}_{idx}"):
            st.session_state["active_sqoff_idx"] = idx
            st.rerun()
        # Only show form for selected row, with correct data
        if show_idx == idx:
            squareoff_form(h, qty, symbol, idx)

if __name__ == "__main__":
    show()
