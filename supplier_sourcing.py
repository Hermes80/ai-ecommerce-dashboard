import urllib.parse

def build_supplier_searches(keyword):
    """
    Build search URLs for AliExpress, Alibaba, and Temu
    based on a keyword or category name.
    This does NOT scrape yet, just returns where to look.
    """
    q = urllib.parse.quote_plus(keyword)

    suppliers = [
        {
            "platform": "AliExpress",
            "search_url": f"https://www.aliexpress.com/wholesale?SearchText={q}"
        },
        {
            "platform": "Alibaba",
            "search_url": f"https://www.alibaba.com/trade/search?SearchText={q}"
        },
        {
            "platform": "Temu",
            "search_url": f"https://www.temu.com/search_result.html?search_key={q}"
        }
    ]
    return suppliers
