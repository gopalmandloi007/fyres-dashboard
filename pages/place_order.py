import streamlit as st
from fyres_utils import place_single_order

def show():
    st.header("Place Single Order (Fyers v3 SDK)")

    symbol = st.text_input("Symbol", "NSE:IDEA-EQ")
    qty = st.number_input("Qty", value=1, step=1, min_value=1)
    
    order_type_tuple = st.selectbox("Order Type", [("Market", 2), ("Limit", 1)], format_func=lambda x: x[0])
    order_type = order_type_tuple[1]
    
    side_tuple = st.selectbox("Side", [("Buy", 1), ("Sell", -1)], format_func=lambda x: x[0])
    side = side_tuple[1]
    
    product_type = st.selectbox("Product Type", ["INTRADAY", "CNC", "CO", "BO"])
    limit_price = st.number_input("Limit Price", value=0.0)
    stop_price = st.number_input("Stop Price", value=0.0)
    validity = st.selectbox("Validity", ["DAY", "IOC"])
    disclosed_qty = st.number_input("Disclosed Qty", value=0, step=1, min_value=0)
    offline_order = st.checkbox("Offline Order", value=False)
    order_tag = st.text_input("Order Tag", "")

    if st.button("Place Order"):
        # Always send at least 1 character for orderTag (Fyers v3 requirement)
        safe_order_tag = order_tag.strip() if order_tag.strip() else "tag1"

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
            "orderTag": safe_order_tag
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

if __name__ == "__main__":
    show()
