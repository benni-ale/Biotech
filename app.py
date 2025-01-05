from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    # Elenco di tutte le aziende
    companies = ['AMGN', 'GILD', 'BIIB', 'VRTX', 'REGN', 'AAPL', 'MSFT', 'GOOGL']  # Esempi di ticker per aziende
    data = {company: yf.Ticker(company).info for company in companies}
    return render_template('index.html', data=data)

@app.route('/biotech')
def biotech():
    # Elenco di aziende biotecnologiche
    biotech_companies = ['AMGN', 'GILD', 'BIIB', 'VRTX', 'REGN']  # Esempi di ticker per aziende biotech
    data = {company: yf.Ticker(company).info for company in biotech_companies}
    return render_template('biotech.html', data=data)

if __name__ == '__main__':
    app.run(debug=True) 