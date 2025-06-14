import streamlit as st
import requests

def get_auth_headers():
    app_id = st.secrets["fyres_app_id"]
    access_token = st.secrets["fyres_access_token"]
    return {"Authorization": f"{app_id}:{access_token}"}

def fyres_get(endpoint, params=None):
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    resp = requests.get(url, headers=headers, params=params)
    try:
        return resp.json()
    except Exception:
        return {}

def fyres_post(endpoint, data=None):
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    headers["Content-Type"] = "application/json"
    resp = requests.post(url, headers=headers, json=data)
    try:
        return resp.json()
    except Exception:
        return {}

def fyres_patch(endpoint, data=None):
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    headers["Content-Type"] = "application/json"
    resp = requests.patch(url, headers=headers, json=data)
    try:
        return resp.json()
    except Exception:
        return {}

def fyres_delete(endpoint, data=None):
    url = f"https://api-t1.fyers.in{endpoint}"
    headers = get_auth_headers()
    headers["Content-Type"] = "application/json"
    resp = requests.delete(url, headers=headers, json=data)
    try:
        return resp.json()
    except Exception:
        return {}
