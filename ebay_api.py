import requests
from access_token import get_access_token
from config import EBAY_REST_URL

# Get fresh access token on each call
def auth_header():
    return {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

# Get active listings
def get_active_listings():
    url = f"{EBAY_REST_URL}/sell/inventory/v1/inventory_item"
    headers = auth_header()

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("LISTINGS ERROR:", response.text)

    return response.json()

# Get orders
def get_orders():
    url = f"{EBAY_REST_URL}/sell/fulfillment/v1/order"
    headers = auth_header()

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("ORDERS ERROR:", response.text)

    return response.json()
