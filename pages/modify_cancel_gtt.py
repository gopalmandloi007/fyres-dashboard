import streamlit as st
from fyres_utils import fyres_patch, fyres_delete

def show():
    st.header("Modify/Cancel GTT Order")
    gtt_id = st.text_input("GTT Order ID to Modify/Cancel")
    action = st.radio("Action", ["Modify", "Cancel"])

    if action == "Modify":
        leg1_price = st.number_input("Leg 1 - New Price", value=0.0)
        leg1_trigger = st.number_input("Leg 1 - New Trigger Price", value=0.0)
        leg1_qty = st.number_input("Leg 1 - New Qty", min_value=1, step=1)
        use_leg2 = st.checkbox("Modify Leg 2 (OCO)?")
        order_info = {"leg1": {"price": float(leg1_price), "triggerPrice": float(leg1_trigger), "qty": int(leg1_qty)}}
        if use_leg2:
            leg2_price = st.number_input("Leg 2 - New Price", value=0.0)
            leg2_trigger = st.number_input("Leg 2 - New Trigger Price", value=0.0)
            leg2_qty = st.number_input("Leg 2 - New Qty", min_value=1, step=1)
            order_info["leg2"] = {"price": float(leg2_price), "triggerPrice": float(leg2_trigger), "qty": int(leg2_qty)}

        if st.button("Modify GTT Order"):
            data = {"id": gtt_id, "orderInfo": order_info}
            resp = fyres_patch("/api/v3/gtt/orders/sync", data)
            st.write(resp)
            if resp.get("s") == "ok":
                st.success("GTT order modified!")
            else:
                st.error(f"Modify failed: {resp.get('message')}")
    else:
        if st.button("Cancel GTT Order"):
            data = {"id": gtt_id}
            resp = fyres_delete("/api/v3/gtt/orders/sync", data)
            st.write(resp)
            if resp.get("s") == "ok":
                st.success("GTT order cancelled!")
            else:
                st.error(f"Cancel failed: {resp.get('message')}")
