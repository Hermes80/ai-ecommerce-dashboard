import time
import json
import requests
from ebay_api import (
    get_active_listings,
    get_orders,
    update_listing_price,
)
from config import (
    EBAY_APP_ID,
    EBAY_CERT_ID,
    EBAY_REFRESH_TOKEN,
    EBAY_OAUTH_URL,
)
import base64

# ======================================================
# Generate Basic Authorization Header
# ======================================================
def base64_credentials():
    creds = f"{EBAY_APP_ID}:{EBAY_CERT_ID}"
    return base64.b64encode(creds.encode()).decode()

# ======================================================
# Get fresh Access Token from Refresh Token
# ======================================================
def get_access_token():
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": EBAY_REFRESH_TOKEN,
        "scope": "https://api.ebay.com/oauth/api_scope"
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + base64_credentials(),
    }

    response = requests.post(EBAY_OAUTH_URL, headers=headers, data=payload)

    if response.status_code != 200:
        print("❌ ERROR refreshing token:", response.text)
        return None

    data = response.json()
    return data.get("access_token")


# ======================================================
# AI Pricing Engine
# ======================================================
def analyze_listing(listing):
    """
    Basic AI pricing logic placeholder
    """
    current_price = float(listing.get("price", 0))
    sell_through = float(listing.get("sell_through_rate", 0))

    new_price = current_price

    if sell_through < 0.3:
        new_price = current_price * 0.97
    elif sell_through > 0.7:
        new_price = current_price * 1.03

    return round(new_price, 2)


# ======================================================
# Main Loop
# ======================================================
def run_engine_loop():
    """
    Runs the AI engine continuously, updating eBay listings.
    """

    while True:
        print("🔄 Refreshing access token...")
        access_token = get_access_token()

        if not access_token:
            print("❌ Could not refresh access token. Retrying in 60 seconds...")
            time.sleep(60)
            continue

        print("🔄 Fetching active listings...")
        listings = get_active_listings(access_token)

        if not listings:
            print("⚠️ No listings found or fetch error.")
        else:
            print(f"📦 Retrieved {len(listings)} listings.")

            for listing in listings:
                new_price = analyze_listing(listing)
                listing_id = listing.get("listing_id")

                if listing_id and new_price:
                    print(f"💲 Updating {listing_id} → New Price {new_price}")
                    update_listing_price(listing_id, new_price, access_token)

        print("⏳ Sleeping 10 minutes...")
        time.sleep(600)


# ======================================================
# Entrypoint
# ======================================================
if __name__ == "__main__":
    print("🤖 Hermes08 AI Engine Started")
    run_engine_loop()
