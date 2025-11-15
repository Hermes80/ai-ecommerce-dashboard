from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

# In-memory log for AI console (simple for now)
ai_command_log = []

# ---------------------------
# LOGIN PROTECTION
# ---------------------------

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

# ---------------------------
# MOCK DATA (SHAPED FOR REAL APIS LATER)
# ---------------------------

def get_dashboard_data():
    # Multi-channel summary (1,2)
    channel_stats = {
        "ebay": {
            "sales_today": 550.00,
            "orders_today": 9,
            "active_listings": 120
        },
        "shopify": {
            "sales_today": 650.00,
            "orders_today": 10,
            "active_listings": 90
        },
        "amazon": {
            "sales_today": 250.00,
            "orders_today": 4,
            "active_listings": 71
        }
    }

    # Overall totals (3,8)
    total_sales_today = sum(ch["sales_today"] for ch in channel_stats.values())
    total_orders_today = sum(ch["orders_today"] for ch in channel_stats.values())
    total_active_listings = sum(ch["active_listings"] for ch in channel_stats.values())

    profit_stats = {
        "revenue_today": total_sales_today,
        "fees_today": round(total_sales_today * 0.12, 2),  # fake 12% fee
        "profit_today": round(total_sales_today * 0.88, 2),
        "margin_percent": 88
    }

    # Time-series data for charts (3,8)
    sales_chart = [200, 400, 600, 450, 900, 700, total_sales_today]
    order_chart = [5, 8, 12, 10, 18, 16, total_orders_today]

    # Simple inventory sample (4)
    inventory = [
        {"sku": "SKU-EB-001", "title": "eBay Test Item 1", "channel": "eBay", "qty": 5, "price": 29.99},
        {"sku": "SKU-SH-010", "title": "Shopify Shirt", "channel": "Shopify", "qty": 2, "price": 39.99},
        {"sku": "SKU-AM-777", "title": "Amazon Gadget", "channel": "Amazon", "qty": 12, "price": 19.99},
        {"sku": "SKU-EB-002", "title": "eBay Test Item 2", "channel": "eBay", "qty": 0, "price": 14.99},
    ]

    data = {
        "total_sales_today": total_sales_today,
        "orders_today": total_orders_today,
        "active_listings": total_active_listings,
        "ai_status": "RUNNING",
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "channel_stats": channel_stats,
        "sales_chart": sales_chart,
        "order_chart": order_chart,
        "inventory": inventory,
        "profit_stats": profit_stats,
        "ai_command_log": ai_command_log[-20:],  # last 20 commands
    }
    return data

# ---------------------------
# ROUTES
# ---------------------------

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "1234":
            session["user"] = "admin"
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/api/data")
@login_required
def data():
    return jsonify(get_dashboard_data())

# AI Command Console (6) – just logs commands for now
@app.route("/api/ai/command", methods=["POST"])
@login_required
def ai_command():
    cmd = request.json.get("command", "").strip()
    if cmd:
        ai_command_log.append({
            "command": cmd,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "queued"  # later you can wire this to your real AI
        })
    return jsonify({"ok": True, "log": ai_command_log[-20:]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
