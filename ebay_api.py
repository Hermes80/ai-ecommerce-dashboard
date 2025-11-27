import requests
from config import EBAY_ACCESS_TOKEN

BASE_URL = "https://api.ebay.com"

def headers():
    return {
        "Authorization": f"Bearer {EBAY_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

def get_active_listings():
    url = f"{BASE_URL}/sell/inventory/v1/inventory_item"
    r = requests.get(url, headers=headers())
    return r.json()

def get_orders():
    url = f"{BASE_URL}/sell/fulfillment/v1/order"
    r = requests.get(url, headers=headers())
    return r.json()
