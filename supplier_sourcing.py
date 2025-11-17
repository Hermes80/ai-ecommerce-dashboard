# supplier_sourcing.py
#
# Searches AliExpress, Alibaba, and Temu
# Using simple placeholder endpoints.
# Replace URLs with real supplier APIs later.

import requests

def find_best_supplier(query):
    """
    Returns best supplier match:
    {
        "source": "AliExpress",
        "title": "...",
        "price": 3.25,
        "url": "..."
    }
    """

    sources = [
        ("AliExpress", f"https://api-supplier.example.com/aliexpress?q={query}"),
        ("Alibaba",    f"https://api-supplier.example.com/alibaba?q={query}"),
        ("Temu",       f"https://api-supplier.example.com/temu?q={query}")
    ]

    best = None

    for name, url in sources:
        try:
            r = requests.get(url, timeout=10)   # <-- Correct line
            if r.status_code != 200:
                continue

            items = r.json().get("results", [])
            for it in items:
                price = float(it.get("price", 9999))

                if best is None or price < best["price"]:
                    best = {
                        "source": name,
                        "title": it.get("title"),
                        "price": price,
                        "url": it.get("url")
                    }

        except Exception:
            continue

    return best or {
        "source": "None",
        "title": "No match found",
        "price": None,
        "url": None
    }
