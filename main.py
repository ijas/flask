from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Webhook data received:", data)
    # Call broker order function here
    return {"status": "received"}, 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
