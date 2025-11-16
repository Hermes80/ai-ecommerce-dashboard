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
