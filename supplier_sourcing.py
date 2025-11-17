# supplier_sourcing.py
#
# Searches AliExpress, Alibaba, and Temu
# using simple keyword-based scraping via RapidAPI-style endpoints.
# You may replace these sample URLs with real supplier APIs.

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
            r = requests.get(url, timeout
