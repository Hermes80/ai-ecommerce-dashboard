import requests

def get_trending_ebay_items(keyword="hot items", max_results=20):
    """
    Very simple 'global' trend fetch using eBay Finding API by keyword.
    This is NOT tied to your account – it's general marketplace data.
    """
    APP_ID = ""  # optional: your eBay app id if you want more control

    url = (
        "https://svcs.ebay.com/services/search/FindingService/v1"
        "?OPERATION-NAME=findItemsByKeywords"
        "&SERVICE-VERSION=1.0.0"
        "&SECURITY-APPNAME={app}".format(app=APP_ID)
        + f"&keywords={keyword}"
        "&RESPONSE-DATA-FORMAT=JSON"
        "&paginationInput.entriesPerPage={}".format(max_results)
    )

    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        items = data["findItemsByKeywordsResponse"][0]["searchResult"][0].get("item", [])
    except Exception:
        items = []

    trending = []
    for it in items:
        trending.append({
            "title": it.get("title", [""])[0],
            "price": float(it.get("sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("__value__", 0)),
            "url": it.get("viewItemURL", [""])[0]
        })

    return trending
