from flask import Flask, request, jsonify
import requests
import time
import hmac
import hashlib
import json
import os

app = Flask(__name__)
DELTA_API_KEY = 'OabPo57OqFxw4Pml6j0lP2bgmiPNYH'
DELTA_API_SECRET = '408CS1n1EWF3qMkdp3JEpJdfZDEc3OtQtXToxqMdX2MbkXbzTsXeMq9oth4t'
BASE_URL = 'https://api.delta.exchange'

def generate_signature(payload, timestamp):
    message = f'{timestamp}{json.dumps(payload)}'
    return hmac.new(DELTA_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()


@app.route('/webhook', methods=['POST'])
def webhook():
    alert = request.json
    print("Received alert:", alert)

    strategy_id = '65xw4Pml6j0lP2bgmi09x'
    side = alert.get("side", "buy")  # "buy" or "sell"
    qty = float(alert.get("qty", 1))
    entry_price = float(alert.get("entry_price"))
    stop_loss = float(alert.get("stop_loss"))
    take_profit = float(alert.get("take_profit"))

    if not strategy_id:
        return jsonify({"error": "strategy_id is required"}), 400

    timestamp = str(int(time.time() * 1000))

    order_payload = {
        "strategy_id": strategy_id,
        "order_type": "entry_order",
        "side": side,
        "size": qty,
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "time_in_force": "gtc"
    }

    signature = generate_signature(order_payload, timestamp)

    headers = {
        "api-key": DELTA_API_KEY,
        "timestamp": timestamp,
        "signature": signature,
        "Content-Type": "application/json"
    }

    url = f"{BASE_URL}/strategies/orders/place"

    try:
        response = requests.post(url, headers=headers, json=order_payload)
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
