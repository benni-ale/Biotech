from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

@app.route('/')
def home():
    # Elenco di aziende biotecnologiche e farmaceutiche
    companies = ['AMGN', 'GILD', 'BIIB', 'VRTX', 'REGN']  # Esempi di ticker per aziende biotech/farmaceutiche
    data = {company: yf.Ticker(company).info for company in companies}
    return render_template('index.html', data=data)

if __name__ == '__main__':
    app.run(debug=True) 