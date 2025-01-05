import requests
from io import BytesIO
from flask import Flask, render_template
import yfinance as yf

app = Flask(__name__)

def get_logo_url(domain, api_key):
    return f'https://img.logo.dev/{domain}?token={api_key}'

@app.route('/')
def home():
    # Elenco di tutte le aziende
    companies = ['AMGN', 'GILD', 'BIIB', 'VRTX', 'REGN', 'AAPL', 'MSFT', 'GOOGL']  # Esempi di ticker per aziende
    api_key = 'pk_Bk503VYEQsGdMJeFjmqxDA'
    
    # Convert stock tickers to website domains
    domains = {company: yf.Ticker(company).info['website'].replace('https://www.', '') for company in companies}  # Remove 'www.'

    data = {
        company: {
            'info': yf.Ticker(company).info,
            'logo_url': get_logo_url(domains[company], api_key)  # Use the new domains variable
        } for company in companies
    }
    return render_template('index.html', data=data)

@app.route('/biotech')
def biotech():
    # Elenco di aziende biotecnologiche
    biotech_companies = ['AMGN', 'GILD', 'BIIB', 'VRTX', 'REGN']  # Esempi di ticker per aziende biotech
    data = {company: yf.Ticker(company).info for company in biotech_companies}
    return render_template('biotech.html', data=data)

if __name__ == '__main__':
    app.run(debug=True) 