from datetime import datetime
from ai_settings import load_settings
from ebay_api import get_active_listings, get_orders, revise_item_price_trading
from supplier_sourcing import build_supplier_searches

def is_live_mode():
    settings = load_settings()
    return settings.get("live_mode", False)


def run_ai_engine():
    """
    Main AI engine entry point.
    Reads settings from ai_settings.json and decides which
    automation blocks to run.
    """
    settings = load_settings()
    ctx = build_context()

    results = []

    # 1) Auto repricing
    if settings.get("auto_reprice"):
        results.append(run_auto_repricing(ctx))

    # 2) Auto listing (stub)
    if settings.get("auto_list"):
        results.append(run_auto_listing(ctx))

    # 3) Supplier sourcing
    if settings.get("auto_source"):
        results.append(run_auto_supplier_sourcing(ctx))

    # 4) Auto ordering (stub)
    if settings.get("auto_order"):
        results.append(run_auto_ordering(ctx))

    # 5) Inventory sync (stub)
    if settings.get("auto_inventory_sync"):
        results.append(run_inventory_sync(ctx))

    # 6) Auto fulfillment (stub)
    if settings.get("auto_fulfill"):
        results.append(run_auto_fulfill(ctx))

    # 7) Buyer messaging (stub)
    if settings.get("auto_message"):
        results.append(run_auto_messaging(ctx))

    # 8) Demand prediction (simple heuristic)
    if settings.get("auto_predict"):
        results.append(run_ai_prediction(ctx))

    # 9) Refund handling (stub)
    if settings.get("auto_refund"):
        results.append(run_auto_refunds(ctx))

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }


# -------------------------------------------------
# Build context: gather marketplace data once
# -------------------------------------------------

def build_context():
    """
    Collects base data the AI needs to make decisions.
    Right now this pulls from eBay only. Shopify/Amazon
    can be added later.
    """
    ebay_listings = get_active_listings()
    ebay_orders = get_orders()

    ctx = {
        "ebay": {
            "listings": ebay_listings,
            "orders": ebay_orders,
        },
        "shopify": {
            "products": [],
            "orders": [],
        },
        "amazon": {
            "products": [],
            "orders": [],
        }
    }
    return ctx


# -------------------------------------------------
# 1) AUTO REPRICING (with optional live mode)
# -------------------------------------------------

def run_auto_repricing(ctx):
    listings = ctx["ebay"]["listings"]
    orders = ctx["ebay"]["orders"]

    sold_item_ids = set()
    for o in orders:
        item_id = o.get("id")
        if item_id:
            sold_item_ids.add(item_id)

    actions = []

    for item in listings:
        item_id = item.get("id")
        title = item.get("title", "Unknown item")
        price_raw = item.get("price", "0")

        try:
            current_price = float(price_raw)
        except ValueError:
            continue

        # Simple rule: if no recent orders, suggest / apply 2% drop
        if item_id not in sold_item_ids:
            new_price = round(current_price * 0.98, 2)

            action = {
                "feature": "auto_reprice",
                "item_id": item_id,
                "title": title,
                "old_price": current_price,
                "new_price": new_price,
                "applied": False,
                "reason": "No recent sales; suggested small price drop."
            }

            if is_live_mode():
    result = revise_item_price_trading(item_id, new_price)
    action["api_result"] = result
    action["applied"] = bool(result.get("success"))

            actions.append(action)

    note_text = (
        "LIVE repricing is ON. Prices were actually sent to eBay."
        if LIVE_REPRICING else
        "LIVE repricing is OFF. These are recommendations only."
    )

    return {
        "feature": "auto_reprice",
        "count": len(actions),
        "actions": actions,
        "note": note_text
    }


# -------------------------------------------------
# 2) AUTO LISTING (stub)
# -------------------------------------------------

def run_auto_listing(ctx):
    return {
        "feature": "auto_list",
        "actions": [],
        "note": "Auto listing not implemented yet. Connect product feeds + listing APIs here."
    }


# -------------------------------------------------
# 3) SUPPLIER SOURCING
# -------------------------------------------------

def run_auto_supplier_sourcing(ctx):
    """
    High-level logic:
    - Look at eBay orders
    - Count categories (or fallback to generic)
    - For top categories, build supplier search URLs
    """
    orders = ctx["ebay"]["orders"]
    category_count = {}

    for o in orders:
        cat = o.get("category", "Unknown")
        category_count[cat] = category_count.get(cat, 0) + 1

    sorted_cats = sorted(category_count.items(), key=lambda x: x[1], reverse=True)

    recommendations = []

    for cat, count in sorted_cats[:5]:
        supplier_links = build_supplier_searches(cat if cat != "Unknown" else "best selling items")
        recommendations.append({
            "feature": "auto_source",
            "category": cat,
            "order_count": count,
            "suppliers": supplier_links,
            "action": "Review these supplier search results and pick best offers."
        })

    return {
        "feature": "auto_source",
        "count": len(recommendations),
        "actions": recommendations,
        "note": "Supplier links generated. Next step: parse prices and compute real ROI."
    }


# -------------------------------------------------
# 4) AUTO ORDERING (stub)
# -------------------------------------------------

def run_auto_ordering(ctx):
    return {
        "feature": "auto_order",
        "actions": [],
        "note": "Auto ordering not implemented yet. Add supplier order API calls here."
    }


# -------------------------------------------------
# 5) INVENTORY SYNC (stub)
# -------------------------------------------------

def run_inventory_sync(ctx):
    return {
        "feature": "auto_inventory_sync",
        "actions": [],
        "note": "Inventory sync not implemented yet. Connect Shopify/Amazon APIs here."
    }


# -------------------------------------------------
# 6) AUTO FULFILLMENT (stub)
# -------------------------------------------------

def run_auto_fulfill(ctx):
    return {
        "feature": "auto_fulfill",
        "actions": [],
        "note": "Auto fulfilment not implemented yet. Add shipment/tracking API calls here."
    }


# -------------------------------------------------
# 7) AUTO MESSAGING (stub)
# -------------------------------------------------

def run_auto_messaging(ctx):
    return {
        "feature": "auto_message",
        "actions": [],
        "note": "Auto buyer messaging not implemented yet. Use marketplace message APIs here."
    }


# -------------------------------------------------
# 8) DEMAND PREDICTION (simple heuristic)
# -------------------------------------------------

def run_ai_prediction(ctx):
    orders = ctx["ebay"]["orders"]
    item_count = {}

    for o in orders:
        item_id = o.get("id")
        if not item_id:
            continue
        item_count[item_id] = item_count.get(item_id, 0) + 1

    ranked = sorted(item_count.items(), key=lambda x: x[1], reverse=True)

    predictions = []
    for item_id, count in ranked[:10]:
        predictions.append({
            "feature": "auto_predict",
            "item_id": item_id,
            "score": count,
            "prediction": "High demand – consider stocking more and improving listing."
        })

    return {
        "feature": "auto_predict",
        "count": len(predictions),
        "actions": predictions,
        "note": "Heuristic prediction. Replace with real ML model if needed."
    }


# -------------------------------------------------
# 9) AUTO REFUNDS (stub)
# -------------------------------------------------

def run_auto_refunds(ctx):
    return {
        "feature": "auto_refund",
        "actions": [],
        "note": "Auto refund logic not implemented yet. Connect to dispute/refund APIs here."
    }
