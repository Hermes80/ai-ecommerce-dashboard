# ai_engine.py
import json
import time
import traceback

from ebay_api import get_active_listings, get_orders
from trend_predictor import predict_trends
from pricing_rules import apply_pricing_rules
from listing_optimizer import optimize_listing
from competitor_detection import detect_competitors
from supplier_sourcing import find_suppliers
from portfolio_builder import build_portfolio

from ai_settings import load_settings


# ---------------------------------------------------------
# REQUIRED BY app.py
# ---------------------------------------------------------

def build_context():
    """
    Build a global AI context.
    app.py calls this during startup.
    """
    try:
        settings = load_settings()

        context = {
            "settings": settings,
            "active_listings": get_active_listings(),
            "orders": get_orders(),
            "trends": predict_trends(),
        }

        return context

    except Exception as e:
        print("❌ Error building AI context:", e)
        traceback.print_exc()
        return {}


def run_ai_loop():
    """
    Main AI engine loop.
    app.py depends on this existing.
    """
    print("🤖 Hermes AI Loop Started")

    while True:
        try:
            # Load latest settings
            settings = load_settings()

            # 1. Fetch platform data
            listings = get_active_listings()
            orders = get_orders()

            # 2. Apply automation
            optimized = []
            for item in listings:
                optimized.append(optimize_listing(item))

            competitors = detect_competitors(listings)
            portfolio = build_portfolio(listings)

            # 3. Output live stats
            print(f"📦 Listings: {len(listings)} | Orders: {len(orders)}")
            print("🔥 Trends:", predict_trends())
            print("🧠 Optimized:", len(optimized))
            print("⚔ Competitor Signals:", len(competitors))

        except Exception as e:
            print("❌ AI Engine Error:", e)
            traceback.print_exc()

        time.sleep(30)   # Runs every 30 seconds


# ---------------------------------------------------------
# OPTIONAL — used by dashboards & CLI
# ---------------------------------------------------------

def run_single_cycle():
    """Runs 1 cycle without looping."""
    ctx = build_context()
    print("Single-cycle AI context:", json.dumps(ctx, indent=2))
    return ctx


if __name__ == "__main__":
    run_ai_loop()
