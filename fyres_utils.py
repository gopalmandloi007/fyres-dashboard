import requests
import streamlit as st

def get_auth_headers():
    app_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return {
        "Authorization": f"{app_id}:{access_token}",
        "Content-Type": "application/json"
    }

def fyres_get(endpoint):
    # Yahan base URL wahi rakhna jo aapke liye sahi chal raha ho (prod ya test)
    url = f"https://api.fyers.in{endpoint}"
    headers = get_auth_headers()
    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        try:
            return {"s": "error", "message": str(e), "raw": resp.text}
        except:
            return {"s": "error", "message": str(e)}

def fyres_post(endpoint, data):
    url = f"https://api.fyers.in{endpoint}"
    headers = get_auth_headers()
    try:
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        try:
            return {"s": "error", "message": str(e), "raw": resp.text}
        except:
            return {"s": "error", "message": str(e)}
