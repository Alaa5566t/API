from flask import Flask, request, jsonify
import ccxt

app = Flask(__name__)

@app.route('/check_balance', methods=['POST'])
def check_balance():
    data = request.json

    if not data:
        return jsonify({"error": "No JSON received"}), 400

    exchange_id = data.get('exchange', '').lower()  # Convert to lowercase
    api_key = data.get('api_key')
    api_secret = data.get('api_secret')

    if not exchange_id or not api_key or not api_secret:
        return jsonify({"error": "Missing parameters"}), 400

    # Check if the exchange exists in CCXT
    if exchange_id not in ccxt.exchanges:
        return jsonify({"error": f"Exchange '{exchange_id}' is not supported by CCXT"}), 400

    try:
        # Initialize the exchange
        exchange_class = getattr(ccxt, exchange_id)
        exchange = exchange_class({
            'apiKey': api_key,
            'secret': api_secret,
            'enableRateLimit': True
        })

        # Manually set API host for MEXC if needed
        if exchange_id == "mexc":
            exchange.urls['api'] = "https://api.mexc.com"

        balance = exchange.fetch_balance()
        return jsonify({"success": True, "balance": balance})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
