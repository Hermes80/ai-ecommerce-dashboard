from flask import Flask, render_template, jsonify
from ai_engine import run_ai_tasks, build_context
from ebay_api import get_active_listings, get_orders

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ai/run")
def ai_run():
    result = run_ai_tasks()
    return jsonify(result)

@app.route("/ebay/listings")
def listings():
    return jsonify(get_active_listings())

@app.route("/ebay/orders")
def orders():
    return jsonify(get_orders())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
