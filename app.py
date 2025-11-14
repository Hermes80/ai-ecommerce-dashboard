from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

def get_mock_stats():
    stats = {
        "total_sales_today": 1234.56,
        "orders_today": 17,
        "active_listings": 245,
        "ai_status": "RUNNING",
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    recent_orders = [
        {"id": "EBAY-1001", "platform": "eBay", "amount": 79.99, "status": "Shipped"},
        {"id": "EBAY-1002", "platform": "eBay", "amount": 24.50, "status": "Paid"},
        {"id": "SHOP-2001", "platform": "Shopify", "amount": 129.00, "status": "Processing"},
        {"id": "AMZ-3001", "platform": "Amazon", "amount": 59.99, "status": "Delivered"},
    ]

    ai_tasks = [
        {"task": "Repricing", "status": "OK", "last_run": "5 min ago"},
        {"task": "Inventory Sync", "status": "OK", "last_run": "10 min ago"},
        {"task": "Order Import", "status": "OK", "last_run": "2 min ago"},
    ]

    return stats, recent_orders, ai_tasks

@app.route("/")
def index():
    stats, recent_orders, ai_tasks = get_mock_stats()
    return render_template("index.html",
                            stats=stats,
                            recent_orders=recent_orders,
                            ai_tasks=ai_tasks)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
