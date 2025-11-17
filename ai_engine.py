from trend_predictor import get_trending_ebay_items
from competitor_detection import get_competitor_prices
from ai_settings import load_settings
from ebay_api import get_active_listings, get_orders, revise_item_price_trading
from supplier_sourcing import build_supplier_searches
from competitor_detection import get_competitor_prices
from pricing_rules import estimate_cost, apply_pricing_rules
from inventory_sync import sync_all_channels

def run_auto_repricing(ctx):
    """
    Dynamic AI repricing:
    - Looks at competitors
    - Applies bulk pricing rules & profit protection
    - Respects live_mode for real updates
    """
    listings = ctx["ebay"]["listings"]
    orders = ctx["ebay"]["orders"]

    sold_item_ids = {o.get("id") for o in orders if o.get("id")}

    actions = []

    for item in listings:
        item_id = item.get("id")
        title = item.get("title", "Unknown")
        try:
            current_price = float(item.get("price", 0))
        except Exception:
            continue

        # 1) Get competitor prices from eBay
        competitors = get_competitor_prices(title)
        competitor_price = None
        if isinstance(competitors, dict) and "error" in competitors:
            competitor_price = None
        else:
            competitor_prices = [c["price"] for c in competitors if c["price"] > 0]
            competitor_price = min(competitor_prices) if competitor_prices else None

        # 2) Initial AI suggestion
        if competitor_price:
            # Start slightly under competitor
            suggested = round(competitor_price - 0.05, 2)

            # If this item *has* sold recently, don't panic-discount
            if item_id in sold_item_ids and suggested < current_price * 0.9:
                suggested = round(current_price * 0.95, 2)
        else:
            # No competitors → gentle 2% drop
            suggested = round(current_price * 0.98, 2)

        # 3) Profit & bulk rules
        cost = estimate_cost(item)
        final_price = apply_pricing_rules(current_price, suggested, cost)

        action = {
            "feature": "auto_reprice",
            "item_id": item_id,
            "title": title,
            "old_price": current_price,
            "competitor_price": competitor_price,
            "suggested_price": suggested,
            "final_price": final_price,
            "cost_estimate": cost,
            "applied": False,
        }

        # 4) Apply to eBay if in live mode
        if is_live_mode():
            result = revise_item_price_trading(item_id, final_price)
            action["api_result"] = result
            action["applied"] = bool(result.get("success"))

        actions.append(action)

    return {
        "feature": "auto_reprice",
        "count": len(actions),
        "actions": actions,
        "note": "Dynamic repricing with competitor detection + profit protection."
    }
        # AI Dynamic Pricing Logic
        
    return {
        "feature": "auto_reprice",
        "count": len(actions),
        "actions": actions,
        "note": "Dynamic AI repricing with competitor detection."
    }
def run_ai_prediction(ctx):
    """
    Global trend-based prediction:
    - Looks at trending items on eBay (not just your account)
    - Returns top items with a simple 'opportunity' tag
    """
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

def run_inventory_sync(ctx):
    actions = sync_all_channels(ctx)
    return {
        "feature": "auto_inventory_sync",
        "count": len(actions),
        "actions": actions,
        "note": "Skeleton inventory sync. Connect Shopify/Amazon APIs inside inventory_sync.py."
            }
from ebay_api import update_price

result = update_price(item_id, item.get("sku"), final_price)
