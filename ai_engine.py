import json
from ai.ai_settings import load_ai_settings

# Import AI modules
from ai.competitor_detection import analyze_competitors
from ai.inventory_sync import sync_inventory
from ai.listing_optimizer import optimize_listings
from ai.trend_predictor import predict_trends
from ai.portfolio_builder import build_portfolio
from ai.supplier_sourcing import find_suppliers
from ai.pricing_rules import apply_pricing_rules

def build_context():
    """Build context object based on AI settings."""
    settings = load_ai_settings()

    return {
        "optimize": settings.get("optimize", True),
        "predict": settings.get("predict", True),
        "sync": settings.get("sync", True),
        "auto_price": settings.get("auto_price", True),
        "auto_source": settings.get("auto_source", True),
        "auto_portfolio": settings.get("auto_portfolio", True),
    }

def run_ai_tasks():
    """Execute all AI engine modules."""
    ctx = build_context()
    results = {}

    if ctx["optimize"]:
        results["optimized_listings"] = optimize_listings()

    if ctx["predict"]:
        results["trend_predictions"] = predict_trends()

    if ctx["sync"]:
        results["inventory_synced"] = sync_inventory()

    if ctx["auto_price"]:
        results["pricing_updates"] = apply_pricing_rules()

    if ctx["auto_source"]:
        results["supplier_suggestions"] = find_suppliers()

    if ctx["auto_portfolio"]:
        results["portfolio"] = build_portfolio()

    return results
