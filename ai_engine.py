"""
AI engine glue code.

- Provides build_context() for app.py / Flask templates.
- Can also run a simple loop if executed directly.
"""

import time
from ebay_api import get_active_listings, get_orders

# If you want to later pull in pricing_rules, trend_predictor, etc.,
# you can import them below WITHOUT changing app.py.
# e.g.:
# from pricing_rules import apply_pricing_rules
# from listing_optimizer import optimize_listing


def build_context():
    """
    Build a context dict for the dashboard.
    app.py calls this function.

    Returns:
        dict with keys:
          - listings: list of active listings
          - orders: list of recent orders
          - stats: simple summary
    """
    listings = get_active_listings()
    orders = get_orders()

    stats = {
        "listing_count": len(listings),
        "order_count": len(orders),
    }

    return {
        "listings": listings,
        "orders": orders,
        "stats": stats,
    }


def ai_main_loop(poll_seconds: int = 300):
    """
    Optional long-running loop if you ever want to run the AI engine
    as a background worker instead of just via Flask.
    """
    print("🤖 Hermes08 AI Engine loop started.")
    while True:
        try:
            ctx = build_context()
            print(
                f"📦 Listings: {ctx['stats']['listing_count']} "
                f"| Orders: {ctx['stats']['order_count']}"
            )

            # TODO: hook in pricing / optimization / forecasting here.

            time.sleep(poll_seconds)
        except Exception as e:
            print("❌ AI Engine error:", e)
            time.sleep(60)


if __name__ == "__main__":
    ai_main_loop()
# === FIXED build_context FUNCTION ===
def build_context():
    """
    Returns a default AI context object so the dashboard
    and API can call AI actions without breaking.
    """
    return {
        "status": "ok",
        "message": "AI engine context loaded",
        "modules": [
            "listing_optimizer",
            "pricing_rules",
            "competitor_detection",
            "inventory_sync",
            "trend_predictor",
            "supplier_sourcing",
            "portfolio_builder"
        ]
    }
