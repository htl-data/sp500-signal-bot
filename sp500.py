import pandas as pd
import requests

def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    table = pd.read_html(response.text)
    df = table[0]
    tickers = df['Symbol'].tolist()
    # Normalize tickers for Yahoo Finance (e.g. BRK.B -> BRK-B)
    tickers = [t.replace('.', '-') for t in tickers]
    return tickers
