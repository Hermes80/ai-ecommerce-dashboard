import requests

def get_competitor_prices(keyword, max_results=10):
    """
    Uses eBay Finding API to fetch competitor listings by keyword.
    """

    APP_ID = ""  # <-- Optional if you have one. Otherwise we use Browse anonymously.

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

        competitors = []
        for it in items:
            competitors.append({
                "title": it.get("title", [""])[0],
                "price": float(it.get("sellingStatus", [{}])[0].get("currentPrice", [{}])[0].get("__value__", 0)),
                "url": it.get("viewItemURL", [""])[0]
            })

        return competitors

    except Exception as e:
        return {"error": str(e)}
