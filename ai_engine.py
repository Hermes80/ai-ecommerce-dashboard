# ai_engine.py
#
# Master AI engine for:
# - repricing
# - competitor detection
# - trend prediction
# - sourcing
# - portfolio builder (via context)
# - inventory sync
#
# Clean, stable, and fully compatible with app.py + portfolio_builder.py

from datetime import datetime
from config import EBAY_OAUTH_TOKEN
from ebay_api import (
    get_active_listings,
    get_orders,
    update_price
)

from competitor_detection import get_competitor_prices
from supplier_sourcing import find_best_supplier
from trend_predictor import get_trending_ebay_items
from inventory_sync import sync_all_channels


# ================================
# Utility: check AI settings
# ================================
from ai_settings import load_settings

def is_live_mode():
    settings = load_settings()
    return bool(settings.get("live_mode", False))


# ================================
# Build AI context (shared data)
# ================================
def build_context():
    listings = get_active_listings()
    orders = get_orders()

    # Build mapping: item_id → number of orders
    sold_map = {}
    for o in orders:
        item_id = o.get("id")
        if item_id:
            sold_map[item_id] = sold_map.get(item_id, 0) + 1

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "ebay": {
            "listings": listings,
            "orders": orders,
            "sold_map": sold_map,
        }
    }


# ================================
# AUTO REPRICING ENGINE
# ================================
def run_ai_reprice(ctx):
    settings = load_settings()
    if not settings.get("auto_reprice", False):
        return {
            "feature": "auto_reprice",
            "count": 0,
            "actions": [],
            "note": "auto_reprice is OFF"
        }

    listings = ctx["ebay"]["listings"]
    sold_map = ctx["ebay"]["sold_map"]

    actions = []

    for item in listings:
        item_id = item.get("id")
        title = item.get("title", "Unknown")
        sku = item.get("sku")
        price = float(item.get("price", 0.0))

        # competitor detection
        competitors = get_competitor_prices(title)
        if isinstance(competitors, dict) and "error" in competitors:
            competitor_price = None
        else:
            competitor_price = competitors[0]["price"] if competitors else None

        # Demand signal
        demand = sold_map.get(item_id, 0)

        # Base logic: competitor-based pricing
        if competitor_price:
            target_price = round(competitor_price - 0.05, 2)

            # Safety: don’t drop more than 10% if item is already selling
            if demand >= 1:
                min_safe = round(price * 0.90, 2)
                if target_price < min_safe:
                    target_price = min_safe
        else:
            # No competitor → slight down adjust
            target_price = round(price * 0.98, 2)

        action = {
            "item_id": item_id,
            "title": title,
            "old_price": price,
            "competitor_price": competitor_price,
            "new_price": target_price,
            "applied": False
        }

        if is_live_mode():
            # Apply via REST first, fallback to Trading API
            result = update_price(item_id, sku, target_price)
            action["api_result"] = result
            action["applied"] = bool(result.get("success"))

        actions.append(action)

    return {
        "feature": "auto_reprice",
        "count": len(actions),
        "actions": actions,
        "note": "Dynamic repricing with competitor detection + profit protection."
    }


# ================================
# AUTO SUPPLIER SOURCING ENGINE
# ================================
def run_ai_sourcing(ctx):
    settings = load_settings()
    if not settings.get("auto_source", False):
        return {
            "feature": "auto_source",
            "count": 0,
            "actions": [],
            "note": "auto_source is OFF"
        }

    listings = ctx["ebay"]["listings"]
    actions = []

    for item in listings:
        title = item.get("title", "Unknown")
        supplier = find_best_supplier(title)

        actions.append({
            "feature": "auto_source",
            "item_id": item.get("id"),
            "title": title,
            "supplier": supplier
        })

    return {
        "feature": "auto_source",
        "count": len(actions),
        "actions": actions,
        "note": "Supplier match from AliExpress, Alibaba, Temu."
    }


# ================================
# TREND PREDICTION ENGINE
# GLOBAL EBAY TRENDS (NOT YOUR ACCOUNT)
# ================================
def run_ai_prediction(ctx):
    settings = load_settings()
    if not settings.get("auto_predict", False):
        return {
            "feature": "auto_predict",
            "count": 0,
            "actions": [],
            "note": "auto_predict is OFF"
        }

    trending = get_trending_ebay_items()
    actions = []

    for t in trending[:20]:
        actions.append({
            "feature": "auto_predict",
            "title": t["title"],
            "price": t["price"],
            "url": t["url"],
            "prediction": "High-trend item on eBay – consider sourcing & listing."
        })

    return {
        "feature": "auto_predict",
        "count": len(actions),
        "actions": actions,
        "note": "Based on global eBay search, not your account data."
    }


# ================================
# INVENTORY SYNC ENGINE (Shopify, Amazon, etc.)
# ================================
def run_inventory_sync(ctx):
    settings = load_settings()
    if not settings.get("auto_inventory_sync", False):
        return {
            "feature": "auto_inventory_sync",
            "count": 0,
            "actions": [],
            "note": "auto_inventory_sync is OFF"
        }

    actions = sync_all_channels(ctx)

    return {
        "feature": "auto_inventory_sync",
        "count": len(actions),
        "actions": actions,
        "note": "Cross-channel inventory sync completed."
    }


# ================================
# MASTER AI ENGINE EXECUTION
# ================================
def run_all_ai_engines():
    ctx = build_context()

    results = []

    results.append(run_ai_reprice(ctx))
    results.append(run_ai_sourcing(ctx))
    results.append(run_ai_prediction(ctx))
    results.append(run_inventory_sync(ctx))

    return {
        "timestamp": datetime.utcnow().isoformat(),
        "results": results
    }
