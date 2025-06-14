import requests
import streamlit as st

# Get API headers from Streamlit secrets
def get_auth_headers():
    app_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return {
        "Authorization": f"{app_id}:{access_token}",
        "Content-Type": "application/json"
    }

# POST to Fyers
def fyres_post(endpoint, data):
    url = f"https://api-t1.fyers.in{endpoint}"
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

# GET from Fyers
def fyres_get(endpoint):
    url = f"https://api-t1.fyers.in{endpoint}"
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

# Fetch LTP (last traded price) for a symbol
def fetch_ltp(symbol):
    data = fyres_get(f"/api/v3/quotes?symbols={symbol}")
    try:
        return float(data["d"][0]["v"]["lp"])
    except Exception:
        return None
