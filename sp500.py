import pandas as pd

def get_sp500_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    table = pd.read_html(url)
    df = table[0]
    tickers = df['Symbol'].tolist()
    # Normalize tickers for Yahoo Finance (e.g. BRK.B -> BRK-B)
    tickers = [t.replace('.', '-') for t in tickers]
    return tickers
