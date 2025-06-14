import streamlit as st
from fyres_utils import fyres_post, fetch_ltp

def get_full_symbol(mid):
    return f"NSE:{mid.strip().upper()}-EQ"

def get_final_qty(qty, amount, price):
    if qty > 0:
        return int(qty)
    elif amount > 0 and price:
        return max(1, int(amount // price))
    else:
        return 0

def show():
    st.header("Place Single Order (Auto Qty/Value)")

    # UI
    symbol_mid = st.text_input("Symbol (e.g. LUMAXIND)", "LUMAXIND")
    side = st.selectbox("Side", [("Buy", 1), ("Sell", 2)], format_func=lambda x: x[0])[1]
    product = st.selectbox("Product", [("CNC", 1), ("INTRADAY", 2), ("CO", 3), ("BO", 4)], format_func=lambda x: x[0])[1]
    order_type = st.selectbox(
        "Order Type",
        [("Limit", 1), ("Market", 2), ("SL-M", 3), ("SL-L", 4)],
        format_func=lambda x: x[0]
    )[1]
    qty = st.number_input("Quantity (set 0 to use Value)", min_value=0, step=1, value=0)
    amount = st.number_input("Value in ₹ (set 0 to use Qty)", min_value=0, value=10000)
    limit_price = st.number_input("Limit Price (for Limit/SL-L)", value=0.0)
    stop_price = st.number_input("Trigger Price (for SL-M/SL-L)", value=0.0)
    order_tag = st.text_input("Order Tag (optional)", "")

    # Symbol and price logic
    symbol_full = get_full_symbol(symbol_mid)
    price_for_calc = None
    if order_type in [1, 4]:  # LIMIT or SL-L
        price_for_calc = limit_price
    else:
        price_for_calc = fetch_ltp(symbol_full)

    computed_qty = get_final_qty(qty, amount, price_for_calc)
    if computed_qty == 0:
        st.warning("Either Quantity or Value must be greater than zero and price must be valid.")
        st.stop()

    # Place order
    if st.button("Place Order"):
        order_data = {
            "symbol": symbol_full,
            "qty": computed_qty,
            "type": order_type,
            "side": 1 if side == 1 else -1,
            "productType": {1: "CNC", 2: "INTRADAY", 3: "CO", 4: "BO"}[product],
            "limitPrice": float(limit_price) if order_type in [1, 4] else 0,
            "stopPrice": float(stop_price) if order_type in [3, 4] else 0,
            "disclosedQty": 0,
            "validity": "DAY",
            "offlineOrder": False
        }
        if order_tag:
            order_data["orderTag"] = order_tag

        st.write("Review Order:", order_data)
        resp = fyres_post("/api/v2/orders", order_data)
        st.write("API Raw Response:", resp)
        if resp.get("code") in [1101, 200] or resp.get("s") == "ok":
            st.success(f"Order Placed! Ref: {resp.get('id', '')}")
        else:
            st.error(f"Order failed: {resp.get('message') or resp.get('raw') or resp}")

# For Streamlit page auto-discovery:
if __name__ == "__main__":
    show()
