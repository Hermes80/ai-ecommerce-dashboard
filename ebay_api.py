import requests
import base64
from config import (
    EBAY_APP_ID,
    EBAY_CERT_ID,
    EBAY_REFRESH_TOKEN,
    EBAY_OAUTH_URL,
    EBAY_REST_URL
)

def base64_credentials():
    raw = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    return base64.b64encode(raw.encode()).decode()

def get_access_token():
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64_credentials()
    }

    response = requests.post(EBAY_OAUTH_URL, headers=headers, data=payload)
    data = response.json()

    if "access_token" not in data:
        print("❌ FAILED TO GET ACCESS TOKEN:", data)
        return None

    return data["access_token"]

def ebay_get(endpoint):
    token = get_access_token()
    if not token:
        return None

    headers = {"Authorization": f"Bearer {token}"}
    url = EBAY_REST_URL + endpoint
    response = requests.get(url, headers=headers)
    return response.json()

def get_active_listings():
    return ebay_get("/sell/inventory/v1/inventory_item")

def get_orders():
    return ebay_get("/sell/fulfillment/v1/order")
