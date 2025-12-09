from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

# =======================================================
# --- ENDPUNKT 1: AKTUELLE DATEN/KENNZAHLEN (info) ---
# =======================================================
@app.route('/api/info/<ticker>', methods=['GET'])
def get_stock_info(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        info_data = stock.info
        return jsonify({"ticker": ticker.upper(), "info": info_data})
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Info-Daten für {ticker}: {str(e)}"}), 500

# =======================================================
# --- ENDPUNKT 2: HISTORISCHE DATEN (history) ---
# =======================================================
@app.route('/api/stock/<ticker>', methods=['GET'])
def get_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        # Letzter Monat
        hist = stock.history(period="1mo")
        # 'records' Orientierung für Zeitreihendaten wie Charts
        data = hist.reset_index().to_json(orient='records', date_format='iso')
        return jsonify({"ticker": ticker.upper(), "data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# =======================================================
# --- ENDPUNKT 3: AKTUELLE NACHRICHTEN (news) ---
# =======================================================
@app.route('/api/news/<ticker>', methods=['GET'])
def get_stock_news(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        news_list = stock.news
        # Begrenzt auf die 5 neuesten Artikel
        return jsonify({"ticker": ticker.upper(), "news": news_list[:5]})
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Nachrichten für {ticker}: {str(e)}"}), 500

# =======================================================
# --- NEU: ENDPUNKT 4: UNTERNEHMENSAKTIONEN (actions) ---
# =======================================================
@app.route('/api/actions/<ticker>', methods=['GET'])
def get_stock_actions(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        actions = stock.actions
        # 'records' Orientierung ist für eine Liste von Aktionen gut
        actions_json = actions.reset_index().to_json(orient='records', date_format='iso')
        return jsonify({"ticker": ticker.upper(), "actions": actions_json})
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Aktionen für {ticker}: {str(e)}"}), 500

# =======================================================
# --- NEU: ENDPUNKT 5: GEWINN- UND VERLUSTRECHNUNG (financials) ---
# =======================================================
@app.route('/api/financials/<ticker>', methods=['GET'])
def get_stock_financials(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        # Jährliche GuV-Daten
        financials = stock.financials
        # 'columns' Orientierung, da die Zeitpunkte die Spaltennamen sind
        financials_json = financials.to_json(orient='columns', date_format='iso')
        return jsonify({"ticker": ticker.upper(), "financials": financials_json})
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der GuV-Daten für {ticker}: {str(e)}"}), 500

# =======================================================
# --- NEU: ENDPUNKT 6: BILANZ (balance_sheet) ---
# =======================================================
@app.route('/api/balance/<ticker>', methods=['GET'])
def get_stock_balance(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        # Jährliche Bilanzdaten
        balance_sheet = stock.balance_sheet
        balance_json = balance_sheet.to_json(orient='columns', date_format='iso')
        return jsonify({"ticker": ticker.upper(), "balance_sheet": balance_json})
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Bilanz-Daten für {ticker}: {str(e)}"}), 500

# =======================================================
# --- NEU: ENDPUNKT 7: CASHFLOW (cashflow) ---
# =======================================================
@app.route('/api/cashflow/<ticker>', methods=['GET'])
def get_stock_cashflow(ticker):
    try:
        stock = yf.Ticker(ticker.upper())
        # Jährliche Cashflow-Daten
        cashflow = stock.cashflow
        cashflow_json = cashflow.to_json(orient='columns', date_format='iso')
        return jsonify({"ticker": ticker.upper(), "cashflow": cashflow_json})
    except Exception as e:
        return jsonify({"error": f"Fehler beim Abrufen der Cashflow-Daten für {ticker}: {str(e)}"}), 500

# =======================================================
# --- ENDPUNKT 8: HEALTH CHECK (home) ---
# =======================================================
@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "Stock API is running", "version": "1.0", "endpoints": ["/api/info/<ticker>", "/api/stock/<ticker>", "/api/news/<ticker>", "/api/actions/<ticker>", "/api/financials/<ticker>", "/api/balance/<ticker>", "/api/cashflow/<ticker>"]}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
