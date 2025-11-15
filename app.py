from flask import Flask, render_template, request, redirect, session, jsonify
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = "super_secret_key_change_this"

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect("/login")
        return f(*args, **kwargs)
    return wrapper

def get_dashboard_data():
    return {
        "total_sales_today": 1450.00,
        "orders_today": 23,
        "active_listings": 281,
        "ai_status": "RUNNING",
        "last_sync": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "sales_chart": [50, 100, 300, 400, 600],
        "order_chart": [1, 3, 4, 5, 10]
    }

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
