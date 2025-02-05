from flask import Flask, request, jsonify
import ccxt

app = Flask(__name__)

@app.route('/check_balance', methods=['POST'])
def check_balance():
    data = request.json
    exchange_id = data['exchange']
    api_key = data['api_key']
    api_secret = data['api_secret']
    
    exchange_class = getattr(ccxt, exchange_id)
    exchange = exchange_class({
        'apiKey': api_key,
        'secret': api_secret,
        'enableRateLimit': True
    })

    try:
        balance = exchange.fetch_balance()
        return jsonify({"success": True, "balance": balance})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)