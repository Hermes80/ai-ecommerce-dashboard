import requests
from requests.auth import HTTPBasicAuth
import xml.etree.ElementTree as ET
from config import (
    EBAY_APP_ID,
    EBAY_CERT_ID,
    EBAY_TOKEN,
    EBAY_OAUTH_URL,
    EBAY_REST_URL,
    EBAY_TRADING_URL
)

# ==========================
# GET OAuth REST Token
# ==========================
def get_oauth_token():
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    r = requests.post(
        EBAY_OAUTH_URL,
        data=data,
        headers=headers,
        auth=HTTPBasicAuth(EBAY_APP_ID, EBAY_CERT_ID)
    )
    if r.status_code == 200:
        return r.json().get("access_token")
    return None

# ==========================
# GET Active Listings (Trading API)
# ==========================
def get_active_listings():
    headers = {
        "X-EBAY-API-CALL-NAME": "GetMyeBaySelling",
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "X-EBAY-API-IAF-TOKEN": EBAY_TOKEN,
        "Content-Type": "text/xml",
    }

    body = """<?xml version="1.0" encoding="utf-8"?>
        <GetMyeBaySellingRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <RequesterCredentials>
                <eBayAuthToken>{}</eBayAuthToken>
            </RequesterCredentials>
            <ActiveList>
                <Include>true</Include>
            </ActiveList>
        </GetMyeBaySellingRequest>
    """.format(EBAY_TOKEN)

    r = requests.post(EBAY_TRADING_URL, data=body, headers=headers)

    items = []
    if r.status_code == 200:
        root = ET.fromstring(r.text)
        ns = {"e": "urn:ebay:apis:eBLBaseComponents"}
        for item in root.findall(".//e:ItemArray/e:Item", ns):
            items.append({
                "title": item.findtext("e:Title", default="", namespaces=ns),
                "price": item.findtext("e:SellingStatus/e:CurrentPrice", default="", namespaces=ns),
                "id": item.findtext("e:ItemID", default="", namespaces=ns),
            })
    return items

# ==========================
# GET Orders (Trading API)
# ==========================
def get_orders():
    headers = {
        "X-EBAY-API-CALL-NAME": "GetOrders",
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "X-EBAY-API-IAF-TOKEN": EBAY_TOKEN,
        "Content-Type": "text/xml",
    }

    body = """<?xml version="1.0" encoding="utf-8"?>
        <GetOrdersRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <RequesterCredentials>
                <eBayAuthToken>{}</eBayAuthToken>
            </RequesterCredentials>
            <OrderRole>Seller</OrderRole>
            <OrderStatus>All</OrderStatus>
        </GetOrdersRequest>
    """.format(EBAY_TOKEN)

    r = requests.post(EBAY_TRADING_URL, data=body, headers=headers)

    orders = []
    if r.status_code == 200:
        root = ET.fromstring(r.text)
        ns = {"e": "urn:ebay:apis:eBLBaseComponents"}
        for o in root.findall(".//e:Order", ns):
            orders.append({
                "id": o.findtext("e:OrderID", default="", namespaces=ns),
                "total": o.findtext("e:Total", default="", namespaces=ns),
                "status": o.findtext("e:OrderStatus", default="", namespaces=ns)
            })
    return orders
# ==========================
# REVISE ITEM PRICE (TRADING API)
# ==========================

def revise_item_price_trading(item_id, new_price):
    """
    Use the Trading API ReviseItem call to change the price
    of a fixed-price listing on eBay.
    This assumes item_id is a valid eBay ItemID and new_price is a float.
    """
    headers = {
        "X-EBAY-API-CALL-NAME": "ReviseItem",
        "X-EBAY-API-SITEID": "0",
        "X-EBAY-API-COMPATIBILITY-LEVEL": "967",
        "X-EBAY-API-IAF-TOKEN": EBAY_TOKEN,
        "Content-Type": "text/xml",
    }

    body = f"""<?xml version="1.0" encoding="utf-8"?>
        <ReviseItemRequest xmlns="urn:ebay:apis:eBLBaseComponents">
            <RequesterCredentials>
                <eBayAuthToken>{EBAY_TOKEN}</eBayAuthToken>
            </RequesterCredentials>
            <Item>
                <ItemID>{item_id}</ItemID>
                <StartPrice>{new_price}</StartPrice>
            </Item>
        </ReviseItemRequest>
    """

    r = requests.post(EBAY_TRADING_URL, data=body, headers=headers)

    if r.status_code != 200:
        return {
            "success": False,
            "status_code": r.status_code,
            "raw": r.text[:500]
        }

    try:
        root = ET.fromstring(r.text)
        ns = {"e": "urn:ebay:apis:eBLBaseComponents"}
        ack = root.findtext("e:Ack", default="", namespaces=ns)
        if ack and ack.upper() == "SUCCESS":
            return {"success": True, "ack": ack}
        else:
            return {"success": False, "ack": ack, "raw": r.text[:500]}
    except Exception as e:
        return {"success": False, "error": str(e), "raw": r.text[:500]}
