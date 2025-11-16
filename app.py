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

 def get_dashboard_data():
    from ebay_api import get_active_listings, get_orders

    # Get eBay data
    ebay_listings = get_active_listings()
    ebay_orders = get_orders()

    # Basic totals
    ebay_sales = len(ebay_orders) * 10.00  # placeholder
    ebay_orders_count = len(ebay_orders)
    ebay_listings_count = len(ebay_listings)

    data = {
        "total_sales_today": ebay_sales,
        "orders_today": ebay_orders_count,
        "active_listings": ebay_listings_count,
        "ai_status": "RUNNING",
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

        "channel_stats": {
            "ebay": {
                "sales_today": ebay_sales,
                "orders_today": ebay_orders_count,
                "active_listings": ebay_listings_count
            },
            "shopify": {"sales_today": 0, "orders_today": 0, "active_listings": 0},
            "amazon":  {"sales_today": 0, "orders_today": 0, "active_listings": 0},
        },

        "sales_chart": [4, 6, 8, 2, ebay_sales],
        "order_chart": [1, 3, 2, 4, ebay_orders_count],

        "inventory": ebay_listings,
        "profit_stats": {
            "revenue_today": ebay_sales,
            "fees_today": round(ebay_sales * 0.12, 2),
            "profit_today": round(ebay_sales * 0.88, 2),
            "margin_percent": 88,
        },

        "ai_command_log": ai_command_log[-20:]
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
