from flask import Flask, request, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return "<h1>Der Server läuft und sendet ALLES! 🚀</h1><p>Nutze /get_stock_data?ticker=AAPL</p>"

@app.route('/get_stock_data')
def get_stock_data():
    ticker_symbol = request.args.get('ticker')
    
    if not ticker_symbol:
        return jsonify({"error": "Kein Ticker angegeben"}), 400

    try:
        stock = yf.Ticker(ticker_symbol)
        
        # WICHTIG: info ruft ALLE oben genannten Daten ab
        all_data = stock.info
        
        # Wir geben das komplette Wörterbuch direkt als JSON zurück
        return jsonify(all_data)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)