# portfolio_builder.py
#
# Smart AI portfolio builder:
# - Scores each of your eBay listings
# - Groups them into CORE / GROWTH / RISKY buckets
# - Adds external "opportunity" ideas from global eBay trends

from pricing_rules import estimate_cost
from competitor_detection import get_competitor_prices
from trend_predictor import get_trending_ebay_items


def score_item(listing, orders_for_item):
    """Return a numeric score + tags for this item."""
    title = listing.get("title", "Unknown")
    price_raw = listing.get("price", 0)

    try:
        price = float(price_raw)
    except Exception:
        price = 0.0

    cost = estimate_cost(listing)
    profit = price - cost
    margin = (profit / price) if price > 0 else 0.0

    # Basic demand signal = how many orders we saw
    demand = len(orders_for_item)

    # Competitor count (simple)
    competitors = get_competitor_prices(title)
    if isinstance(competitors, dict) and "error" in competitors:
        comp_count = 0
    else:
        comp_count = len(competitors)

    # Simple scoring formula:
    # - reward demand
    # - reward margin
    # - punish heavy competition
    score = demand * 3 + margin * 10 - comp_count * 0.5

    tags = []
    if demand >= 5:
        tags.append("High Demand")
    elif demand >= 2:
        tags.append("Moderate Demand")
    else:
        tags.append("Low Demand")

    if margin >= 0.4:
        tags.append("High Margin")
    elif margin >= 0.2:
        tags.append("Good Margin")
    else:
        tags.append("Thin Margin")

    if comp_count >= 10:
        tags.append("Crowded Niche")
    elif comp_count <= 3:
        tags.append("Low Competition")

    return {
        "score": round(score, 2),
        "margin_percent": round(margin * 100, 1),
        "competitors": comp_count,
        "demand": demand,
        "profit_estimate": round(profit, 2),
        "tags": tags,
        "price": round(price, 2),
        "cost_estimate": round(cost, 2),
    }


def categorize_item(score_dict):
    """Return a bucket name for this item based on its score & margin."""
    score = score_dict["score"]
    margin = score_dict["margin_percent"]
    demand = score_dict["demand"]

    # Core: good demand + margin + decent score
    if score >= 10 and margin >= 25 and demand >= 3:
        return "core"

    # Growth: decent score, some demand, room to grow
    if score >= 5 and demand >= 1:
        return "growth"

    # Risky: low score or very thin margin
    return "risky"


def build_portfolio(ctx):
    """
    Build a full portfolio view:
    - core: strong products
    - growth: promising ones
    - risky: weak / experimental
    - external_opportunities: global eBay trends to consider adding
    """
    listings = ctx["ebay"]["listings"]
    orders = ctx["ebay"]["orders"]

    # Group orders by item id
    orders_by_item = {}
    for o in orders:
        oid = o.get("id")
        if oid:
            orders_by_item.setdefault(oid, []).append(o)

    core = []
    growth = []
    risky = []

    for listing in listings:
        item_id = listing.get("id")
        title = listing.get("title", "Unknown")

        item_orders = orders_by_item.get(item_id, [])
        stats = score_item(listing, item_orders)

        portfolio_entry = {
            "id": item_id,
            "title": title,
            "price": stats["price"],
            "score": stats["score"],
            "margin_percent": stats["margin_percent"],
            "competitors": stats["competitors"],
            "demand": stats["demand"],
            "profit_estimate": stats["profit_estimate"],
            "tags": stats["tags"],
        }

        bucket = categorize_item(stats)
        if bucket == "core":
            core.append(portfolio_entry)
        elif bucket == "growth":
            growth.append(portfolio_entry)
        else:
            risky.append(portfolio_entry)

    # Sort each bucket by score descending
    core.sort(key=lambda x: x["score"], reverse=True)
    growth.sort(key=lambda x: x["score"], reverse=True)
    risky.sort(key=lambda x: x["score"], reverse=True)

    # External global opportunities (not yet in your store)
    external = []
    trending = get_trending_ebay_items()
    for t in trending[:20]:
        external.append({
            "title": t["title"],
            "price": t["price"],
            "url": t["url"],
            "note": "High-trend item on global eBay. Consider sourcing & listing."
        })

    return {
        "core": core,
        "growth": growth,
        "risky": risky,
        "external_opportunities": external,
  }
