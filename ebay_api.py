import requests
import xml.etree.ElementTree as ET
from config import (
    EBAY_APP_ID,
    EBAY_CERT_ID,
    EBAY_OAUTH_TOKEN,
    EBAY_API_ENDPOINT,
    EBAY_REST_ENDPOINT,
)

# -------------------------------------------------------
# 1) Get Active Listings (Sell Inventory or Trading API)
# -------------------------------------------------------

def get_active_listings():
    """
    Try Sell Inventory API first.
    If it fails, fall back to Trading API.
    """

    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    url = f"{EBAY_REST_ENDPOINT}/sell/inventory/v1/inventory_item"

    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            data = r.json()
            items = []

            for product in data.get("inventoryItems", []):
                item_sku = product.get("sku")
                price_info = product.get("product", {}).get("aspects", {})
                price = None

                # Extract price if present
                offers = product.get("offerId")
                if offers:
                    price = offers.get("price")

                items.append({
                    "id": item_sku,
                    "title": product.get("product", {}).get("title", "No Title"),
                    "price": price or 0,
                    "sku": item_sku,
                    "quantity": product.get("availability", {}).get("shipToLocationAvailability", {}).get("quantity", 1),
                })

            if items:
                return items

    except Exception:
        pass  # Continue to Trading fallback

    # -------------------------
    # Trading API fallback
    # -------------------------

    headers = {
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "X-EBAY-API-CALL-NAME": "GetMyeBaySelling",
        "Content-Type": "text/xml"
    }

    xml = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <GetMyeBaySellingRequest xmlns="urn:ebay:apis:eBLBaseComponents">
      <RequesterCredentials>
        <eBayAuthToken>{EBAY_OAUTH_TOKEN}</eBayAuthToken>
      </RequesterCredentials>
      <ActiveList>
        <Include>true</Include>
      </ActiveList>
    </GetMyeBaySellingRequest>
    """

    try:
        r = requests.post(EBAY_API_ENDPOINT, data=xml, headers=headers, timeout=20)
        root = ET.fromstring(r.text)

        items = []
        namespace = "{urn:ebay:apis:eBLBaseComponents}"

        for it in root.findall(f".//{namespace}Item"):
            item_id = it.findtext(f"{namespace}ItemID")
            title = it.findtext(f"{namespace}Title")
            price = it.find(f"{namespace}StartPrice")
            price_value = float(price.text) if price is not None else 0.0

            items.append({
                "id": item_id,
                "title": title,
                "price": price_value,
            })

        return items

    except Exception:
        return []


# -------------------------------------------------------
# 2) Get Orders (Sell Fulfillment API)
# -------------------------------------------------------

def get_orders():
    """
    Pull real orders from Sell Fulfillment API.
    """

    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    url = f"{EBAY_REST_ENDPOINT}/sell/fulfillment/v1/order"

    try:
        r = requests.get(url, headers=headers, timeout=15)

        if r.status_code != 200:
            return []

        data = r.json()
        orders = []

        for order in data.get("orders", []):
            orders.append({
                "id": order.get("orderId"),
                "price": order.get("pricingSummary", {}).get("total", {}).get("value", 0),
                "category": "Unknown",
            })

        return orders

    except Exception:
        return []


# -------------------------------------------------------
# 3) Update Prices via Trading API
# -------------------------------------------------------

def revise_item_price_trading(item_id, new_price):
    headers = {
        "X-EBAY-API-CALL-NAME": "ReviseFixedPriceItem",
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "Content-Type": "text/xml",
    }

    xml = f"""
    <?xml version="1.0" encoding="utf-8"?>
    <ReviseFixedPriceItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
      <RequesterCredentials>
        <eBayAuthToken>{EBAY_OAUTH_TOKEN}</eBayAuthToken>
      </RequesterCredentials>
      <Item>
        <ItemID>{item_id}</ItemID>
        <StartPrice>{new_price}</StartPrice>
      </Item>
    </ReviseFixedPriceItemRequest>
    """

    try:
        r = requests.post(EBAY_API_ENDPOINT, data=xml, headers=headers)
        if "<Ack>Success</Ack>" in r.text:
            return {"success": True, "price": new_price}
        return {"success": False, "raw": r.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


# -------------------------------------------------------
# 4) Update Prices via Sell Inventory API
# -------------------------------------------------------

def revise_item_price_inventory(sku, new_price):
    headers = {
        "Authorization": f"Bearer {EBAY_OAUTH_TOKEN}",
        "Content-Type": "application/json",
        "X-EBAY-C-MARKETPLACE-ID": "EBAY_US"
    }

    url = f"{EBAY_REST_ENDPOINT}/sell/inventory/v1/offer/{sku}/update_price_quantity"

    body = {
        "price": {
            "value": str(new_price),
            "currency": "USD"
        }
    }

    try:
        r = requests.post(url, json=body, headers=headers)
        if r.status_code in (200, 201):
            return {"success": True, "price": new_price}
        return {"success": False, "raw": r.text}
    except Exception as e:
        return {"success": False, "error": str(e)}


# -------------------------------------------------------
# 5) Main update_price() used by AI
# -------------------------------------------------------

def update_price(item_id, sku, new_price):
    """
    Try Inventory API first (REST).
    If fails, fall back to Trading API.
    """

    # Try REST
    if sku:
        result = revise_item_price_inventory(sku, new_price)
        if result.get("success"):
            return {"method": "REST", **result}

    # Fallback: Trading
    result = revise_item_price_trading(item_id, new_price)
    return {"method": "Trading", **result}
