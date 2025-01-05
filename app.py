import requests
from io import BytesIO
from flask import Flask, render_template
import yfinance as yf
import matplotlib.pyplot as plt
import base64

# Imposta il backend di Matplotlib su 'Agg' per l'uso non interattivo
plt.switch_backend('Agg')

app = Flask(__name__)

def get_logo_url(domain, api_key):
    return f'https://img.logo.dev/{domain}?token={api_key}'

def generate_stock_plot(ticker):
    stock_data = yf.Ticker(ticker).history(period="3mo")
    plt.figure(figsize=(2, 1))
    plt.plot(stock_data.index, stock_data['Close'], color='blue')
    plt.axis('off')  # Nascondi assi
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

@app.route('/')
def home():
    # Elenco di tutte le aziende
    companies = ['AMGN', 'GILD', 'BIIB', 'VRTX', 'REGN', 'AAPL', 'MSFT', 'GOOG']  # Esempi di ticker per aziende
    api_key = 'pk_Bk503VYEQsGdMJeFjmqxDA'
    
    # Converti i ticker delle azioni in domini web
    domains = {company: yf.Ticker(company).info['website'].replace('https://www.', '') for company in companies}  # Rimuovi 'www.'

    data = {
        company: {
            'info': yf.Ticker(company).info,
            'logo_url': get_logo_url(domains[company], api_key),
            'plot': generate_stock_plot(company)  # Genera grafico per ciascuna azienda
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