import requests
from io import BytesIO
from flask import Flask, render_template
import yfinance as yf
import matplotlib.pyplot as plt
import base64

# Testing Fork for push

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

def format_market_cap(value):
    """Format market cap to a human-readable string."""
    if value >= 1_000_000_000_000:
        return f'${value / 1_000_000_000_000:.3f} T'  # Trillions
    elif value >= 1_000_000_000:
        return f'${value / 1_000_000_000:.3f} B'  # Billions
    elif value >= 1_000_000:
        return f'${value / 1_000_000:.3f} M'  # Millions
    else:
        return f'${value}'  # Less than a million

def generate_market_cap_plot(ticker):
    # Fetch historical market cap data (you may need to adjust this based on your data source)
    market_cap_data = yf.Ticker(ticker).history(period="1y")  # Get 1 year of historical data
    plt.figure(figsize=(10, 5))
    plt.plot(market_cap_data.index, market_cap_data['Close'], color='green', label='Market Cap')
    plt.title(f'Market Cap Trend for {ticker}')
    plt.xlabel('Date')
    plt.ylabel('Market Cap ($)')
    plt.legend()
    plt.grid()
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    plt.close()
    buf.seek(0)
    return base64.b64encode(buf.getvalue()).decode('utf8')

def get_historical_market_cap(ticker):
    # Fetch historical market cap data for the last 5 years
    market_cap_data = yf.Ticker(ticker).history(period="5y")  # Get 5 years of historical data
    return market_cap_data.index.year.tolist(), market_cap_data['Close'].tolist()  # Return only the years

@app.route('/')
def home():
    # Elenco di tutte le aziende
    companies = ['AMGN', 'GILD', 'BIIB', 'VRTX', 'REGN', 'AAPL', 'MSFT', 'GOOG']  # Esempi di ticker per aziende
    api_key = 'pk_Bk503VYEQsGdMJeFjmqxDA'
    
    # Converti i ticker delle azioni in domini web
    domains = {
        company: yf.Ticker(company).info['website'].replace('https://www.', '') if company != 'GOOG' else 'google.com'
        for company in companies
    }  # Rimuovi 'www.' per tutte le aziende tranne Google

    data = {
        company: {
            'info': yf.Ticker(company).info,
            'logo_url': get_logo_url(domains[company], api_key),
            'plot': generate_stock_plot(company),  # Genera grafico per ciascuna azienda
            'marketCap': format_market_cap(yf.Ticker(company).info.get('marketCap', 0)),  # Format market cap
        } for company in companies
    }
    return render_template('index.html', data=data)

@app.route('/biotech')
def biotech():
    # Elenco di aziende biotecnologiche
    biotech_companies = ['AMGN', 'GILD', 'BIIB', 'VRTX', 'REGN']  # Esempi di ticker per aziende biotech
    data = {company: yf.Ticker(company).info for company in biotech_companies}
    return render_template('biotech.html', data=data)

@app.route('/company/<symbol>')
def company_detail(symbol):
    company_name = yf.Ticker(symbol).info['shortName']
    description = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."
    dates, market_cap_values = get_historical_market_cap(symbol)  # Get historical market cap data
    return render_template('company_detail.html', company_name=company_name, description=description, dates=dates, market_cap_values=market_cap_values)

if __name__ == '__main__':
    app.run(debug=True) 