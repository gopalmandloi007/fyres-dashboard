import streamlit as st
from utils import get_fyers_client

PRODUCT_MAP = {1: "CNC", 2: "INTRADAY", 3: "CO", 4: "BO"}
ORDER_TYPE_MAP = {1: "LIMIT", 2: "MARKET", 3: "SL-M", 4: "SL-L"}
SIDE_MAP = {1: "BUY", 2: "SELL"}

def get_full_symbol(mid):
    return f"NSE:{mid.upper()}-EQ"

def fetch_ltp(fyers, symbol):
    try:
        data = {"symbols": symbol}
        quote = fyers.quotes(data)
        ltp = float(quote['d'][0]['v']['lp'])
        return ltp
    except Exception as e:
        st.warning(f"Could not fetch LTP for {symbol}: {e}")
        return None

def show():
    st.header("Place Order (FYERS)")
    fyers = get_fyers_client()

    symbol_mid = st.text_input("Symbol (MID)", value="LUMAXIND")
    side = st.selectbox("Side", options=list(SIDE_MAP.keys()), format_func=lambda x: SIDE_MAP[x], index=0)
    product = st.selectbox("Product", options=list(PRODUCT_MAP.keys()), format_func=lambda x: PRODUCT_MAP[x], index=0)
    order_type = st.selectbox("Order Type", options=list(ORDER_TYPE_MAP.keys()), format_func=lambda x: ORDER_TYPE_MAP[x], index=0)
    qty = st.number_input("Quantity (set 0 to use Value)", min_value=0, value=1)
    amount = st.number_input("Value (₹, set 0 to use Qty)", min_value=0, value=0)
    limit_price = st.number_input("Limit Price", min_value=0.0, value=0.0)
    stop_price = st.number_input("Stop Price", min_value=0.0, value=0.0)
    order_tag = st.text_input("Order Tag (optional)", value="")

    def get_final_qty(qty, amount, price):
        if qty > 0:
            return int(qty)
        elif amount > 0:
            if price in [None, 0]:
                return 0
            return max(1, int(amount // price))
        else:
            return 0

    symbol_full = get_full_symbol(symbol_mid)
    price_for_calc = None
    if order_type in [1, 4]:
        price_for_calc = limit_price
    else:
        price_for_calc = fetch_ltp(fyers, symbol_full)
    computed_qty = get_final_qty(qty, amount, price_for_calc)

    if st.button("Place Order"):
        if computed_qty == 0:
            st.error("Specify either quantity or value/amount greater than zero!")
            return

        order = {
            "symbol": symbol_full,
            "qty": int(computed_qty),
            "type": 1 if SIDE_MAP[side] == "BUY" else 2,
            "side": 1 if SIDE_MAP[side] == "BUY" else -1,
            "productType": PRODUCT_MAP[product],
            "orderType": ORDER_TYPE_MAP[order_type],
            "limitPrice": float(limit_price) if ORDER_TYPE_MAP[order_type] in ["LIMIT", "SL-L"] else 0,
            "stopPrice": float(stop_price) if ORDER_TYPE_MAP[order_type] in ["SL-M", "SL-L"] else 0,
            "disclosedQty": 0,
            "validity": "DAY",
            "offlineOrder": False
        }
        if order_tag:
            order["orderTag"] = order_tag

        response = fyers.place_order(order)
        st.write("Order Response:", response)
        if response.get("code") in [200, 1101]:
            st.success(f"✅ Order Successful! Order ID: {response.get('id','')}")
        else:
            st.error(f"❌ Order Failed! {response.get('message', '')}")
