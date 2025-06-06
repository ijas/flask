from flask import Flask, jsonify
import os

app = Flask(__name__)


@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        data = request.json
        print("Webhook received:", data)
        return 'POST received', 200
    return 'Webhook endpoint is live', 200


if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
