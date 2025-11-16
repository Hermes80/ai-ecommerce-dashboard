from datetime import datetime
from ai_settings import load_settings
from ebay_api import get_active_listings, get_orders

def run_ai_engine():
    """
    Main AI engine entry point.
    It reads settings from ai_settings.json and decides which
    automation blocks to run.
    """
    settings = load_settings()
    ctx = build_context()

    results = []

    # 1) Auto repricing
    if settings.get("auto_reprice"):
        results.append(run_auto_repricing(ctx))

    # 2) Auto listing (placeholder)
    if settings.get("auto_list"):
        results.append(run_auto_listing(ctx))

    # 3) Auto supplier sourcing
    if settings.get("auto_source"):
        results.append(run_auto_supplier_sourcing(ctx))

    # 4) Auto ordering (placeholder)
    if settings.get("auto_order"):
        results.append(run_auto_ordering(ctx))

    # 5) Inventory sync (placeholder)
    if settings.get("auto_inventory_sync"):
        results.append(run_inventory_sync(ctx))

    # 6) Auto fulfilment (placeholder)
    if settings.get("auto_fulfill"):
        results.append(run_auto_fulfill(ctx))

    # 7) Buyer messaging (placeholder)
    if settings.get("auto_message"):
        results.append(run_auto_messaging(ctx))

    # 8) Demand prediction
    if settings.get("auto_predict"):
        results.append(run_ai_prediction(ctx))

    # 9) Refund handling (placeholder)
    if settings.get("auto_refund"):
        results.append(run_auto_refunds(ctx))

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": results
    }


# -------------------------------------------------
# Build context: gather data once, reuse it in all
# -------------------------------------------------

def build_context():
    """
    Collects base data the AI needs to make decisions.
    Right now this pulls from eBay only. Shopify/Amazon
    hooks can be added later.
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
# 1) AUTO REPRICING
# -------------------------------------------------

def run_auto_repricing(ctx):
    """
    Very simple example:
    - Look at eBay listings
    - Suggest dropping price by 2% on items with no orders
    This returns a list of RECOMMENDED price updates.
    Later you can wire this into a real eBay ReviseItem call.
    """
    listings = ctx["ebay"]["listings"]
    orders = ctx["ebay"]["orders"]

    # Build a set of itemIDs that HAVE sold recently
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
            # skip if we can't parse price
            continue

        if item_id not in sold_item_ids:
            new_price = round(current_price * 0.98, 2)  # 2% drop
            actions.append({
                "feature": "auto_reprice",
                "item_id": item_id,
                "title": title,
                "old_price": current_price,
                "new_price": new_price,
                "reason": "No recent sales; suggested small price drop."
            })

    return {
        "feature": "auto_reprice",
        "count": len(actions),
        "actions": actions,
        "note": "These are recommendations. Wire to real eBay ReviseItem API when ready."
    }


# -------------------------------------------------
# 2) AUTO LISTING (placeholder)
# -------------------------------------------------

def run_auto_listing(ctx):
    """
    Placeholder: in future this would:
    - Find winning products from supplier feeds
    - Create draft listings on eBay/Shopify/Amazon
    For now we just return a stub message.
    """
    return {
        "feature": "auto_list",
        "actions": [],
        "note": "Auto listing logic not implemented yet. Add product feed + create listing APIs here."
    }


# -------------------------------------------------
# 3) SUPPLIER SOURCING (high-level logic)
# -------------------------------------------------

def run_auto_supplier_sourcing(ctx):
    """
    High-level sourcing logic:
    - Look at eBay best-sellers / orders
    - Identify what categories sell best
    - (Later) Query supplier APIs to find matching products
    """
    orders = ctx["ebay"]["orders"]
    category_count = {}

    for o in orders:
        # This is a placeholder; you can extend your ebay_api.get_orders
        # to include category / SKU info and aggregate here.
        cat = o.get("category", "Unknown")
        category_count[cat] = category_count.get(cat, 0) + 1

    sorted_cats = sorted(category_count.items(), key=lambda x: x[1], reverse=True)

    recommendations = []
    for cat, count in sorted_cats[:5]:
        recommendations.append({
            "feature": "auto_source",
            "category": cat,
            "order_count": count,
            "action": "Search suppliers for more items in this category."
        })

    return {
        "feature": "auto_source",
        "count": len(recommendations),
        "actions": recommendations,
        "note": "Wire this to real supplier APIs (AliExpress, Alibaba, etc.) to fetch offers."
    }


# -------------------------------------------------
# 4) AUTO ORDERING (placeholder)
# -------------------------------------------------

def run_auto_ordering(ctx):
    """
    Placeholder auto ordering:
    - In a real system, this would:
      * Check low-stock items
      * Place orders with preferred suppliers
    """
    return {
        "feature": "auto_order",
        "actions": [],
        "note": "Auto ordering not implemented yet. Add supplier ordering API calls here."
    }


# -------------------------------------------------
# 5) INVENTORY SYNC (placeholder)
# -------------------------------------------------

def run_inventory_sync(ctx):
    """
    Placeholder inventory sync.
    Later this would compare inventory across:
    - eBay
    - Shopify
    - Amazon
    and push consistent stock levels.
    """
    return {
        "feature": "auto_inventory_sync",
        "actions": [],
        "note": "Inventory sync not implemented yet. Connect to Shopify/Amazon APIs here."
    }


# -------------------------------------------------
# 6) AUTO FULFILLMENT (placeholder)
# -------------------------------------------------

def run_auto_fulfill(ctx):
    """
    Placeholder auto fulfilment:
    - Would mark orders as shipped and add tracking
      using marketplace APIs.
    """
    return {
        "feature": "auto_fulfill",
        "actions": [],
        "note": "Auto fulfilment not implemented yet. Add shipment + tracking API calls here."
    }


# -------------------------------------------------
# 7) AUTO MESSAGING (placeholder)
# -------------------------------------------------

def run_auto_messaging(ctx):
    """
    Placeholder auto messaging logic.
    In a real system, this could:
    - Send 'thanks for your order' messages
    - Follow-up messages
    - Request feedback
    """
    return {
        "feature": "auto_message",
        "actions": [],
        "note": "Auto buyer messaging not implemented yet. Use marketplace message APIs here."
    }


# -------------------------------------------------
# 8) DEMAND PREDICTION (simple heuristic)
# -------------------------------------------------

def run_ai_prediction(ctx):
    """
    Very simple 'prediction':
    - Count orders per item
    - Sort by volume
    - Flag top items as 'high demand'
    Later you can plug in a real ML model here.
    """
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
        "note": "Basic heuristic prediction. Replace with real ML model if needed."
    }


# -------------------------------------------------
# 9) AUTO REFUNDS (placeholder)
# -------------------------------------------------

def run_auto_refunds(ctx):
    """
    Placeholder refund logic.
    Later this could:
    - Inspect disputes
    - Auto-approve small refunds
    - Escalate large ones for manual review
    """
    return {
        "feature": "auto_refund",
        "actions": [],
        "note": "Auto refund logic not implemented yet. Connect to dispute/refund APIs here."
    }
