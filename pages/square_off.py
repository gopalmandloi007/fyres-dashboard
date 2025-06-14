import streamlit as st
from fyres_utils import fetch_holdings, place_single_order
import re

def get_alphanumeric(text, default="tag1"):
    cleaned = re.sub(r'[^A-Za-z0-9]', '', text)
    return cleaned if cleaned else default

def sell_form(stock, idx):
    unique_id = f"{stock['symbol']}_{idx}"
    st.markdown("---")
    with st.form(f"sell_form_{unique_id}"):
        symbol = st.text_input("Symbol", stock["symbol"], key=f"symbol_{unique_id}")
        qty = st.number_input(
            "Qty", min_value=1, max_value=int(stock["quantity"]), value=int(stock["quantity"]), key=f"qty_{unique_id}"
        )
        order_type_tuple = st.selectbox(
            "Order Type", [("Market", 2), ("Limit", 1)], format_func=lambda x: x[0], key=f"ordertype_{unique_id}"
        )
        order_type = order_type_tuple[1]
        side = -1  # Always Sell for square off
        product_type = st.selectbox("Product Type", ["CNC", "INTRADAY", "CO", "BO"], index=0, key=f"ptype_{unique_id}")
        limit_price = st.number_input(
            "Limit Price", value=float(stock.get("ltp", 0.0)), min_value=0.0, key=f"lprice_{unique_id}"
        )
        stop_price = st.number_input("Stop Price", value=0.0, key=f"stop_{unique_id}")
        validity = st.selectbox("Validity", ["DAY", "IOC"], key=f"validity_{unique_id}")
        disclosed_qty = st.number_input(
            "Disclosed Qty", min_value=0, max_value=int(qty), value=0, key=f"disclose_{unique_id}"
        )
        offline_order = st.checkbox("Offline Order", value=False, key=f"offline_{unique_id}")
        order_tag_raw = st.text_input("Order Tag", value=f"sell{stock['symbol'].replace('-','').replace(':','')}", key=f"tag_{unique_id}")
        order_tag = get_alphanumeric(order_tag_raw, default="tag1")

        submitted = st.form_submit_button("Place Order")
        if submitted:
            order_data = {
                "symbol": symbol,
                "qty": int(qty),
                "type": order_type,
                "side": side,
                "productType": product_type,
                "limitPrice": float(limit_price),
                "stopPrice": float(stop_price),
                "validity": validity,
                "disclosedQty": int(disclosed_qty),
                "offlineOrder": offline_order,
                "orderTag": order_tag
            }
            if order_type == 2:  # Market
                order_data["limitPrice"] = 0
                order_data["stopPrice"] = 0

            st.write("Order Review:", order_data)
            try:
                resp = place_single_order(order_data)
                st.write("API Response:", resp)
                if resp.get("s") == "ok":
                    st.success(f"Order Placed! Ref: {resp.get('id', '')}")
                else:
                    st.error(f"Order Failed: {resp.get('message', '')}")
            except Exception as e:
                st.error(f"Exception: {e}")

def show():
    st.header("Square Off Holdings (Fyers v3 SDK style)")
    resp = fetch_holdings()
    holdings = resp.get("holdings", [])
    if not holdings:
        st.info("No holdings found.")
        return

    st.markdown("#### Your Holdings")
    columns = st.columns([2, 1, 1, 1, 1])
    for i, label in enumerate(["Symbol", "Qty", "LTP", "Avg Price", "Sell"]):
        columns[i].markdown(f"**{label}**")
    sell_id = st.session_state.get("sell_id", None)

    for idx, stock in enumerate(holdings):
        symbol = stock.get("symbol", "")
        qty = int(stock.get("quantity", 0))
        ltp = stock.get("ltp", 0)
        avg_price = stock.get("avg_price", 0)
        columns = st.columns([2, 1, 1, 1, 1])
        columns[0].write(symbol)
        columns[1].write(qty)
        columns[2].write(ltp)
        columns[3].write(avg_price)
        if columns[4].button("Sell", key=f"sell_btn_{idx}"):
            st.session_state["sell_id"] = idx
            st.rerun()
        if sell_id == idx:
            sell_form(stock, idx)

if __name__ == "__main__":
    show()
