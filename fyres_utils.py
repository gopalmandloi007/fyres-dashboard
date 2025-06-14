import streamlit as st
import requests

def get_auth_headers():
    app_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return {"Authorization": f"{app_id}:{access_token}"}

def fyres_post(endpoint, data=None):
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    headers["Content-Type"] = "application/json"
    try:
        resp = requests.post(url, headers=headers, json=data)
        st.write("Request URL:", url)
        st.write("Request Headers:", headers)
        st.write("Request Data:", data)
        st.write("Raw Response Text:", resp.text)
        try:
            return resp.json()
        except Exception:
            return {"s": "error", "message": "Invalid JSON", "raw": resp.text}
    except Exception as e:
        return {"s": "error", "message": str(e)}
