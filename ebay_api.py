import requests
from config import EBAY_ACCESS_TOKEN, EBAY_REST_URL

# ==========================================================
# eBay API Helpers
# ==========================================================
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {EBAY_ACCESS_TOKEN}"
}

# ----------------------------------------------------------
# Get Active Listings
# ----------------------------------------------------------
def get_active_listings():
    url = f"{EBAY_REST_URL}/sell/inventory/v1/inventory_item"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("inventoryItems", [])
    else:
        print("❌ Error fetching active listings:", response.text)
        return []

# ----------------------------------------------------------
# Get Orders
# ----------------------------------------------------------
def get_orders():
    url = f"{EBAY_REST_URL}/sell/fulfillment/v1/order"
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        return response.json().get("orders", [])
    else:
        print("❌ Error fetching orders:", response.text)
        return []
