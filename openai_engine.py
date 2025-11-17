# openai_engine.py
#
# GPT-4.1 “brain” for your StorePilot dashboard.
# This powers your existing AI console and gives it many skills:
# - Product research
# - Listing creation
# - Competitor analysis
# - Supplier ideas
# - Pricing strategy
# - Portfolio advice (core / growth / risky)
# - Forecasting & business coaching

from typing import List, Dict, Any
from openai import OpenAI

from config import OPENAI_API_KEY, OPENAI_MODEL
from ai_engine import build_context

client = OpenAI(api_key=OPENAI_API_KEY)


def _summarize_listings(listings: List[Dict[str, Any]], max_items: int = 15) -> str:
    """
    Make a short text snapshot of current listings for the AI.
    We only send a small sample so we don't blow up tokens.
    """
    lines = []
    for item in listings[:max_items]:
        title = item.get("title", "Unknown")
        price = item.get("price", 0)
        sku = item.get("sku", "")
        item_id = item.get("id", "")
        lines.append(f"- {title} | ${price} | sku={sku} | id={item_id}")
    return "\n".join(lines) if lines else "No active listings found."


def _summarize_orders(orders: List[Dict[str, Any]], max_items: int = 15) -> str:
    lines = []
    for o in orders[:max_items]:
        oid = o.get("id", "unknown")
        price = o.get("price", 0)
        cat = o.get("category", "Unknown")
        lines.append(f"- order_id={oid} | ${price} | category={cat}")
    return "\n".join(lines) if lines else "No recent orders found."


def build_store_snapshot() -> str:
    """
    Build a compact snapshot of your store for GPT-4.1 to reason about.
    """
    ctx = build_context()
    listings = ctx["ebay"]["listings"]
    orders = ctx["ebay"]["orders"]

    snapshot = f"""
    Store snapshot:
    - Active listings: {len(listings)}
    - Orders in memory: {len(orders)}

    Sample listings:
    { _summarize_listings(listings) }

    Sample orders:
    { _summarize_orders(orders) }
    """
    # Trim whitespace nicely
    return "\n".join(line.rstrip() for line in snapshot.strip().splitlines())


def run_ai_chat(user_message: str) -> str:
    """
    Main entry point used by /api/ai/chat.
    Take whatever the user typed in the console and respond intelligently.
    The same endpoint handles:
    - "What should I sell?"
    - "Create a listing for X"
    - "Analyze my competitors for X"
    - "Build a portfolio plan"
    - "Forecast my revenue"
    - "Give me a weekly action plan"
    and more.
    """

    store_snapshot = build_store_snapshot()

    system_prompt = f"""
    You are StorePilot Pro, an AI ecommerce operator for eBay (and future channels).
    You help the user with:

    1) PRODUCT RESEARCH
       - Suggest specific product ideas to sell.
       - Use eBay-style thinking: demand, competition, price range.
       - Explain WHY each product is a good or bad idea.

    2) LISTING CREATION
       - Given a product idea, generate:
         * A strong eBay title (max ~80 chars).
         * 5 bullet points.
         * A detailed but clear description.
         * Suggested price range (USD).
         * Suggested item specifics / keywords.

    3) COMPETITOR & PRICING ANALYSIS
       - Help user think about how to price vs competitors.
       - Suggest when to undercut, match, or price higher with value.

    4) SUPPLIER & MARGIN IDEAS
       - Suggest what to look for on AliExpress / Alibaba / Temu.
       - Estimate rough landed cost ranges.
       - Show how to get a safe profit margin.

    5) PORTFOLIO THINKING (CORE / GROWTH / RISKY)
       - CORE: safe, recurring, stable items.
       - GROWTH: promising mid-risk products.
       - RISKY: high upside, high competition / volatility.
       - Help the user balance their mix.

    6) FORECASTING & STRATEGY
       - Roughly forecast which ideas could move more units.
       - Suggest weekly action plans:
         * what to list
         * what to test
         * what to drop
         * what to raise prices on.

    7) GENERAL BUSINESS COACH
       - Explain concepts simply.
       - Give specific, actionable advice (no fluff).
       - When uncertain, say what data would be needed.

    You have this store snapshot (partial, not perfect):

    {store_snapshot}

    Rules:
    - Speak in simple, direct language.
    - Prefer bullet points and short sections.
    - Always give concrete next steps.
    - If the user asks something vague like "Upgrade AI" or "What now?",
      respond with a practical to-do list tailored to ecommerce.
    - If you reference numbers (margins, prices), make them reasonable estimates,
      not guarantees.
    """

    completion = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        temperature=0.35,
    )

    reply = completion.choices[0].message.content
    return reply
