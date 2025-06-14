import streamlit as st
import requests

def get_auth_headers():
    """Returns the authorization headers required for Fyres API."""
    app_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return {"Authorization": f"{app_id}:{access_token}"}

def fyres_get(endpoint, params=None):
    """Performs a GET request to the Fyres API."""
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    try:
        resp = requests.get(url, headers=headers, params=params)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"s": "error", "message": str(e), "raw": getattr(resp, "text", "")}

def fyres_post(endpoint, data=None):
    """Performs a POST request to the Fyres API."""
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    headers["Content-Type"] = "application/json"
    try:
        resp = requests.post(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        # Return error details and raw response if available
        return {"s": "error", "message": str(e), "raw": getattr(resp, "text", "")}

def fyres_patch(endpoint, data=None):
    """Performs a PATCH request to the Fyres API."""
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    headers["Content-Type"] = "application/json"
    try:
        resp = requests.patch(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"s": "error", "message": str(e), "raw": getattr(resp, "text", "")}

def fyres_delete(endpoint, data=None):
    """Performs a DELETE request to the Fyres API."""
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    headers["Content-Type"] = "application/json"
    try:
        resp = requests.delete(url, headers=headers, json=data)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"s": "error", "message": str(e), "raw": getattr(resp, "text", "")}
