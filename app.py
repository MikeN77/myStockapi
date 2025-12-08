from flask import Flask, jsonify
from flask_cors import CORS 
import yfinance as yf
# Hinweis: Die 'json'-Bibliothek ist für dieses Setup nicht zwingend notwendig
# import json 

app = Flask(__name__)
CORS(app) 

# =======================================================
# --- ENDPUNKT 1: HISTORISCHE DATEN (ALT) ---
# =======================================================
@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        hist = stock.history(period="1mo")
        
        # Konvertiert das Pandas DataFrame in JSON, kompatibel mit JavaScript
        # Wichtig: Wir speichern hier den JSON-STRING im 'data'-Feld.
        data = hist.reset_index().to_json(orient='records', date_format='iso')
        
        return jsonify({
            "ticker": ticker.upper(), 
            "data": data
        })
    except Exception as e:
        # Gibt eine HTTP 500 Fehlermeldung mit der Fehlerbeschreibung zurück
        return jsonify({"error": str(e)}), 500

# =======================================================
# --- ENDPUNKT 2: AKTUELLE NACHRICHTEN (NEU) ---
# =======================================================
@app.route('/api/news/<ticker>', methods=['GET'])
def get_stock_news(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        
        # Ruft die Liste der News-Dictionaries ab. yfinance liefert sie bereits als Python-Liste.
        news_list = stock.news
        
        # jsonify konvertiert die Python-Liste direkt in ein JSON-Array.
        return jsonify({
            "ticker": ticker.upper(),
            # Begrenzt die Ausgabe auf die 10 neuesten Artikel zur Übersicht
            "news": news_list[:10]
        })
    except Exception as e:
        # Gibt eine HTTP 500 Fehlermeldung zurück
        return jsonify({"error": f"Fehler beim Abrufen der Nachrichten für {ticker}: {str(e)}"}), 500


if __name__ == '__main__':
    # Stellt sicher, dass Sie den Debug-Modus verwenden, um Fehler direkt zu sehen
    app.run(debug=True, port=5000)
