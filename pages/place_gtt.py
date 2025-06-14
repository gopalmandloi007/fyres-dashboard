import streamlit as st
from fyres_utils import place_gtt_order

def show():
    st.header("Place GTT Order (Single/OCO)")

    symbol = st.text_input("Symbol", "NSE:SBIN-EQ")
    side = st.selectbox("Side", [("Buy", 1), ("Sell", -1)], format_func=lambda x: x[0])[1]
    product_type = st.selectbox("Product Type", ["CNC", "MARGIN", "MTF"])

    # Leg 1
    st.subheader("Leg 1 (Required)")
    price1 = st.number_input("Leg 1 Price", value=100.0)
    trigger_price1 = st.number_input("Leg 1 Trigger Price", value=100.0)
    qty1 = st.number_input("Leg 1 Qty", value=1, min_value=1, step=1)

    oco = st.checkbox("OCO (add stop-loss/target leg)?", value=False)

    # Leg 2 (OCO)
    price2 = trigger_price2 = qty2 = None
    if oco:
        st.subheader("Leg 2 (Optional, for OCO)")
        price2 = st.number_input("Leg 2 Price", value=90.0)
        trigger_price2 = st.number_input("Leg 2 Trigger Price", value=90.0)
        qty2 = st.number_input("Leg 2 Qty", value=1, min_value=1, step=1)

    if st.button("Place GTT Order"):
        order_data = {
            "side": side,
            "symbol": symbol,
            "productType": product_type,
            "orderInfo": {
                "leg1": {
                    "price": price1,
                    "triggerPrice": trigger_price1,
                    "qty": int(qty1)
                }
            }
        }
        if oco:
            order_data["orderInfo"]["leg2"] = {
                "price": price2,
                "triggerPrice": trigger_price2,
                "qty": int(qty2)
            }
        resp = place_gtt_order(order_data)
        st.write("API Response:", resp)
        if resp.get("s") == "ok":
            st.success(f"Order placed! ID: {resp.get('id')}")
        else:
            st.error(f"Error: {resp.get('message')}")

if __name__ == "__main__":
    show()
