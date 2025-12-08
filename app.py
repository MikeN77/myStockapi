from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
import json # Für die Datenverarbeitung

app = Flask(__name__)
CORS(app) 

# --- ENDPUNKT 1: HISTORISCHE DATEN (Bereits vorhanden) ---
@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        # ... (der Code für historische Daten bleibt hier)
        hist = stock.history(period="1mo")
        data = hist.reset_index().to_json(orient='records', date_format='iso')
        return jsonify({"ticker": ticker.upper(), "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ----------------------------------------------------
# --- NEUER ENDPUNKT 2: NACHRICHTEN HINZUFÜGEN ---
# ----------------------------------------------------
@app.route('/api/news/<ticker>', methods=['GET'])
def get_stock_news(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        
        # Ruft die Liste der News-Dictionaries ab
        news_list = stock.news
        
        # Begrenzen Sie die Ausgabe auf z.B. die 10 neuesten Artikel
        # und formatieren Sie es so, dass es direkt als JSON gesendet werden kann
        
        return jsonify({
            "ticker": ticker.upper(),
            "news": news_list[:10]
        })
    except Exception as e:
        # Hier fangen wir Fehler ab, z.B. wenn der Ticker nicht gefunden wird
        return jsonify({"error": f"Fehler beim Abrufen der Nachrichten für {ticker}: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
