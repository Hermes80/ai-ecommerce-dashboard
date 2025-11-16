from competitor_detection import get_competitor_prices

def run_auto_repricing(ctx):
    listings = ctx["ebay"]["listings"]
    orders = ctx["ebay"]["orders"]

    sold_item_ids = {o.get("id") for o in orders if o.get("id")}

    actions = []

    for item in listings:
        item_id = item.get("id")
        title = item.get("title", "Unknown")
        price = float(item.get("price", 0))

        competitors = get_competitor_prices(title)

        if isinstance(competitors, dict) and "error" in competitors:
            competitor_price = None
        else:
            competitor_prices = [c["price"] for c in competitors if c["price"] > 0]
            competitor_price = min(competitor_prices) if competitor_prices else None

        # AI Dynamic Pricing Logic
        if competitor_price:
            # Target slightly below competitor
            target_price = round(competitor_price - 0.05, 2)

            # Safety: don’t drop more than 10% unless item is cold
            if target_price < price * 0.9 and item_id in sold_item_ids:
                target_price = round(price * 0.95, 2)

        else:
            # No competitors → fallback rule
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
            result = revise_item_price_trading(item_id, target_price)
            action["api_result"] = result
            action["applied"] = bool(result.get("success"))

        actions.append(action)

    return {
        "feature": "auto_reprice",
        "count": len(actions),
        "actions": actions,
        "note": "Dynamic AI repricing with competitor detection."
    }
