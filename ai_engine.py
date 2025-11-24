import json
import time
import requests
from datetime import datetime
from competitor_detection import analyze_competitors
from listing_optimizer import optimize_listing
from trend_predictor import predict_trends
from pricing_rules import apply_pricing_rules
from supplier_sourcing import find_suppliers
from inventory_sync import sync_inventory
from portfolio_builder import rebalance_portfolio
from config import (
    EBAY_APP_ID,
    EBAY_CERT_ID,
    EBAY_REFRESH_TOKEN,
    EBAY_OAUTH_URL,
    EBAY_REST_URL
)
from ebay_api import get_active_listings, get_orders


# -----------------------------------------
#   TOKEN HANDLING: DYNAMIC ACCESS TOKEN
# -----------------------------------------

def base64_credentials():
    import base64
    creds = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    return base64.b64encode(creds.encode()).decode()


def get_access_token():
    """Generate a fresh eBay OAuth Access Token using the REFRESH TOKEN."""
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/sell.inventory"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64_credentials()
    }

    response = requests.post(EBAY_OAUTH_URL, headers=headers, data=payload)

    if response.status_code != 200:
        print("Failed to refresh access token:", response.text)
        return None

    return response.json().get("access_token")


# -------------------------------------------------
#   HERMES08 AI ENGINE: MAIN AUTOMATION FUNCTIONS
# -------------------------------------------------

def analyze_listings():
    """Pull all active listings and run AI analysis."""
    access_token = get_access_token()
    if not access_token:
        return {"error": "Unable to generate access token"}

    listings = get_active_listings(access_token)
    if "error" in listings:
        return listings

    results = []
    for item in listings.get("listings", []):
        item_result = {
            "item_id": item.get("itemId"),
            "title": item.get("title"),
            "optimization": optimize_listing(item),
            "competitor_analysis": analyze_competitors(item),
            "trend_prediction": predict_trends(item),
        }
        results.append(item_result)

    return {"results": results}


def process_orders():
    """Fetch orders and run automation workflows."""
    access_token = get_access_token()
    if not access_token:
        return {"error": "Unable to generate access token"}

    orders = get_orders(access_token)
    if "error" in orders:
        return orders

    processed = []
    for order in orders.get("orders", []):
        processed.append({
            "orderId": order.get("orderId"),
            "status": order.get("orderFulfillmentStatus"),
            "buyer": order.get("buyerUsername
