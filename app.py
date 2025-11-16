from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime
from functools import wraps
from ebay_api import get_active_listings, get_orders
from ai_settings import load_settings, update_setting
from ai_settings import load_settings
from ebay_api import get_active_listings, get_orders
from datetime import datetime
from ai_settings import load_settings
from ebay_api import get_active_listings, get_orders
from datetime import datetime
from supplier_sourcing import build_supplier_searches
from listing_optimizer import optimize_title, optimize_description

def run_ai_engine():
    settings = load_settings()

    actions = []

    # 1. AUTO PRICING
    if settings.get("auto_reprice"):
        actions.append(run_auto_repricing())

    # 2. AUTO LISTING
    if settings.get("auto_list"):
        actions.append(run_auto_listing())

    # 3. AUTO SUPPLIER SOURCING
    if settings.get("auto_source"):
        actions.append(run_auto_supplier_sourcing())

    # 4. AUTO ORDERING
    if settings.get("auto_order"):
        actions.append(run_auto_ordering())

    # 5. AUTO INVENTORY SYNC
    if settings.get("auto_inventory_sync"):
        actions.append(run_inventory_sync())

    # 6. AUTO FULFILL
    if settings.get("auto_fulfill"):
        actions.append(run_auto_fulfill())

    # 7. AUTO MESSAGE BUYERS
    if settings.get("auto_message"):
        actions.append(run_auto_messaging())

    # 8. AUTO TREND PREDICTION
    if settings.get("auto_predict"):
        actions.append(run_ai_prediction())

    # 9. AUTO REFUNDS
    if settings.get("auto_refund"):
        actions.append(run_auto_refunds())

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": actions
    }

# -------------------------
#  PLACEHOLDER AI FUNCTIONS
#  (we will fill these with real logic next)
# -------------------------

def run_auto_repricing():
    return "Auto-repricing executed."

def run_auto_listing():
    return "AI auto-listing executed."

def run_auto_supplier_sourcing():
    return "AI sourced new suppliers based on demand."

def run_auto_ordering():
    return "AI placed supplier orders."

def run_inventory_sync():
    return "Inventory sync completed."

def run_auto_fulfill():
    return "Orders auto-fulfilled."

def run_auto_messaging():
    return "Buyers auto-messaged."

def run_ai_prediction():
    return "AI demand forecasting executed."

def run_auto_refunds():
    return "Refund operations executed."
def run_ai_engine():
    settings = load_settings()

    actions = []

    # 1. AUTO PRICING
    if settings.get("auto_reprice"):
        actions.append(run_auto_repricing())

    # 2. AUTO LISTING
    if settings.get("auto_list"):
        actions.append(run_auto_listing())

    # 3. AUTO SUPPLIER SOURCING
    if settings.get("auto_source"):
        actions.append(run_auto_supplier_sourcing())

    # 4. AUTO ORDERING
    if settings.get("auto_order"):
        actions.append(run_auto_ordering())

    # 5. AUTO INVENTORY SYNC
    if settings.get("auto_inventory_sync"):
        actions.append(run_inventory_sync())

    # 6. AUTO FULFILL
    if settings.get("auto_fulfill"):
        actions.append(run_auto_fulfill())

    # 7. AUTO MESSAGE BUYERS
    if settings.get("auto_message"):
        actions.append(run_auto_messaging())

    # 8. AUTO TREND PREDICTION
    if settings.get("auto_predict"):
        actions.append(run_ai_prediction())

    # 9. AUTO REFUNDS
    if settings.get("auto_refund"):
        actions.append(run_auto_refunds())

    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": actions
    }

# -------------------------
#  PLACEHOLDER AI FUNCTIONS
#  (we will fill these with real logic next)
# -------------------------

def run_auto_repricing():
    return "Auto-repricing executed."

def run_auto_listing():
    return "AI auto-listing executed."

def run_auto_supplier_sourcing():
    return "AI sourced new suppliers based on demand."

def run_auto_ordering():
    return "AI placed supplier orders."

def run_inventory_sync():
    return "Inventory sync completed."

def run_auto_fulfill():
    return "Orders auto-fulfilled."

def run_auto_messaging():
    return "Buyers auto-messaged."

def run_ai_prediction():
    return "AI demand forecasting executed."

def run_auto_refunds():
    return "Refund operations executed."
app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

ai_command_log = []

# ---------------------------
# DASHBOARD DATA (REAL EBAY)
# ---------------------------

def get_dashboard_data():
    ebay_listings = get_active_listings()
    ebay_orders = get_orders()

    ebay_sales = len(ebay_orders) * 10.00
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
# LOGIN SYSTEM
# ---------------------------

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

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

# ---------------------------
# MAIN DASHBOARD
# ---------------------------

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/api/data")
@login_required
def data():
    return jsonify(get_dashboard_data())


@app.route("/ai-chat")
@login_required
def ai_chat_page():
    return render_template("ai_chat.html")


@app.route("/api/ai/chat", methods=["POST"])
@login_required
def ai_chat_api():
    user_msg = request.json.get("message", "")
    if not user_msg:
        return jsonify({"reply": "Please type something."})

    reply = f"You said: {user_msg}. Real AI is coming."

    return jsonify({"reply": reply})
@app.route("/ai-settings")
@login_required
def ai_settings_page():
    settings = load_settings()
    return render_template("ai_settings.html", settings=settings)


@app.route("/api/ai/settings/update", methods=["POST"])
@login_required
def ai_settings_update():
    data = request.json
    key = data.get("key")
    value = data.get("value")

    if key not in load_settings():
        return jsonify({"error": "Invalid setting"}), 400

    new_settings = update_setting(key, value)
    return jsonify({"success": True, "settings": new_settings})


@app.route("/api/ai/run", methods=["POST"])
@login_required
def ai_run():
    result = run_ai_engine()
    return jsonify(result)  

@app.route("/suppliers")
@login_required
def suppliers_page():
    return render_template("suppliers.html")

@app.route("/api/suppliers")
@login_required
def suppliers_api():
    from ai_engine import run_auto_supplier_sourcing, build_context
    ctx = build_context()
    result = run_auto_supplier_sourcing(ctx)
    return jsonify(result)

@app.route("/api/ai/optimize-listing", methods=["POST"])
@login_required
def ai_optimize_listing():
    data = request.json or {}
    title = data.get("title", "")
    description = data.get("description", "")

    new_title = optimize_title(title)
    new_desc = optimize_description(description)

    return jsonify({
        "old_title": title,
        "new_title": new_title,
        "old_description": description,
        "new_description": new_desc
    })
# ---------------------------
# AI Console
# ---------------------------

@app.route("/api/ai/command", methods=["POST"])
@login_required
def ai_command():
    cmd = request.json.get("command", "").strip()
    if cmd:
        ai_command_log.append({
            "command": cmd,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "queued"
        })
    return jsonify({"ok": True, "log": ai_command_log[-20:]})

# ---------------------------
# START SERVER
# ---------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
