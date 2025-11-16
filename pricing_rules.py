# pricing_rules.py
#
# Central place for all pricing rules, profit protection and bulk repricing logic.

MIN_PROFIT_MARGIN = 0.20   # 20% minimum profit margin
MAX_DISCOUNT_PERCENT = 0.30  # never reduce more than 30% vs current price
MIN_PRICE_ABSOLUTE = 5.00    # never price below this hard floor


def estimate_cost(item):
    """
    Estimate item cost.

    If your ebay_api.get_active_listings() returns a 'cost' field,
    we use that. Otherwise we assume cost = 60% of current selling price.
    """
    price_raw = item.get("price", 0)
    try:
        price = float(price_raw)
    except Exception:
        price = 0.0

    cost_raw = item.get("cost")
    if cost_raw is not None:
        try:
            return float(cost_raw)
        except Exception:
            pass

    # Default assumption: cost ~ 60% of price
    return round(price * 0.6, 2)


def apply_pricing_rules(current_price, suggested_price, cost):
    """
    Apply safety rules to the AI-suggested price:
    - enforce minimum absolute price
    - enforce minimum profit margin
    - limit max discount vs current price
    """

    # Hard floor
    if suggested_price < MIN_PRICE_ABSOLUTE:
        suggested_price = MIN_PRICE_ABSOLUTE

    # Limit discount vs current price
    min_allowed_price = current_price * (1 - MAX_DISCOUNT_PERCENT)
    if suggested_price < min_allowed_price:
        suggested_price = round(min_allowed_price, 2)

    # Profit margin check
    if cost > 0:
        profit = suggested_price - cost
        if suggested_price > 0:
            margin = profit / suggested_price
        else:
            margin = 0.0

        if margin < MIN_PROFIT_MARGIN:
            # Push price up to meet margin requirement
            target_price = cost / (1 - MIN_PROFIT_MARGIN)
            suggested_price = round(max(suggested_price, target_price), 2)

    # Final floor again
    if suggested_price < MIN_PRICE_ABSOLUTE:
        suggested_price = MIN_PRICE_ABSOLUTE

    return round(suggested_price, 2)
