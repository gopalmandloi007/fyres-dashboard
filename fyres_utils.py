import streamlit as st
import requests

def get_auth_headers():
    app_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return {"Authorization": f"{app_id}:{access_token}"}

def fyres_get(endpoint, params=None):
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"s": "error", "message": str(e), "raw": getattr(resp, "text", "")}
