from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf
import os

app = Flask(__name__)
CORS(app) # Erlaubt Zugriff von deiner WebApp

@app.route('/stock')
def get_stock():
    ticker_symbol = request.args.get('ticker')
    if not ticker_symbol:
        return jsonify({"error": "Bitte ?ticker= symbol angeben"}), 400

    try:
        stock = yf.Ticker(ticker_symbol)
        # Wir holen die 'info' (Kennzahlen)
        info = stock.info
        
        # Wir bauen ein sauberes Paket für deine App
        data = {
            "name": info.get('shortName'),
            "price": info.get('currentPrice') or info.get('regularMarketPrice'),
            "currency": info.get('currency'),
            "dividendYield": info.get('dividendYield'),
            "exDate": info.get('exDividendDate'), # Timestamp
            "payoutRatio": info.get('payoutRatio'),
            "forwardPE": info.get('forwardPE') # Kurs-Gewinn-Verhältnis
        }
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render vergibt den Port dynamisch
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)