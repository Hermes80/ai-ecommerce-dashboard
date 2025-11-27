import requests
from config import EBAY_ACCESS_TOKEN, EBAY_REST_URL

# Basic headers for all eBay Sell API calls
def _headers():
    return {
        "Authorization": f"Bearer {EBAY_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

# ---------- Active Listings ----------
def get_active_listings():
    """
    Fetch inventory items from eBay Sell Inventory API.
    """
    url = f"{EBAY_REST_URL}/sell/inventory/v1/inventory_item"
    resp = requests.get(url, headers=_headers())

    if resp.status_code == 200:
        data = resp.json()
        return data.get("inventoryItems", [])
    else:
        print("❌ Error fetching active listings:", resp.status_code, resp.text)
        return []

# ---------- Orders ----------
def get_orders():
    """
    Fetch orders from eBay Sell Fulfillment API.
    """
    url = f"{EBAY_REST_URL}/sell/fulfillment/v1/order"
    resp = requests.get(url, headers=_headers())

    if resp.status_code == 200:
        data = resp.json()
        return data.get("orders", [])
    else:
        print("❌ Error fetching orders:", resp.status_code, resp.text)
        return []
