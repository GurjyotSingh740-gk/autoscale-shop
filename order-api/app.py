from flask import Flask, request, jsonify, render_template
import time, random
from prometheus_flask_exporter import PrometheusMetrics   # ← This line must be 

app = Flask(__name__)
metrics = PrometheusMetrics(app)  # ← This one line adds /metrics endpoint

# Custom metric — order counter
orders_placed = metrics.counter(
    'orders_placed_total',
    'Total number of orders placed'
)

orders = []

@app.route('/')
def home():
    return render_template('index.html', orders=orders)

@app.route('/order', methods=['POST'])
def place_order():
    data = request.json
    order_id = random.randint(1000, 9999)
    order = {"id": order_id, "item": data.get("item", "Unknown"), "qty": data.get("qty", 1)}
    orders.append(order)
    # Simulate CPU load for HPA demo
    time.sleep(0.05)
    return jsonify({"status": "Order placed", "order": order}), 201

@app.route('/orders', methods=['GET'])
def get_orders():
    return jsonify(orders)

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)