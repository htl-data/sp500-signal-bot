def get_sp500_tickers():
    """Return S&P 500 tickers. Uses Wikipedia with fallback to hardcoded core list."""
    try:
        import requests
        import pandas as pd
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        tables = pd.read_html(resp.text)
        df = tables[0]
        tickers = df['Symbol'].tolist()
        tickers = [t.replace('.', '-') for t in tickers]
        print(f'Loaded {len(tickers)} tickers from Wikipedia')
        return tickers
    except Exception as e:
        print(f'Wikipedia fetch failed ({e}), using fallback list')
        return _fallback_tickers()


def _fallback_tickers():
    """Core S&P 500 tickers hardcoded as fallback."""
    return [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'GOOGL', 'META', 'TSLA', 'BRK-B', 'JPM', 'UNH',
        'V', 'XOM', 'LLY', 'MA', 'AVGO', 'HD', 'CVX', 'MRK', 'ABBV', 'COST',
        'PEP', 'KO', 'BAC', 'ADBE', 'WMT', 'MCD', 'CSCO', 'CRM', 'ACN', 'TMO',
        'ABT', 'ORCL', 'DHR', 'LIN', 'NFLX', 'AMD', 'TXN', 'NEE', 'PM', 'QCOM',
        'BMY', 'UPS', 'AMGN', 'LOW', 'INTU', 'MS', 'GS', 'CAT', 'BA', 'SPGI',
        'BLK', 'ELV', 'SYK', 'GILD', 'AXP', 'MDLZ', 'ADI', 'DE', 'ISRG', 'VRTX',
        'LMT', 'C', 'ZTS', 'CI', 'MMC', 'PLD', 'ADP', 'REGN', 'CVS', 'SO',
        'MO', 'DUK', 'NOC', 'USB', 'TJX', 'ITW', 'CL', 'SHW', 'PNC', 'MMM',
        'F', 'GM', 'GE', 'WFC', 'RTX', 'EMR', 'FDX', 'NSC', 'ETN', 'EOG',
        'HCA', 'MCO', 'KLAC', 'LRCX', 'PSA', 'CME', 'AON', 'ECL', 'APD', 'ICE',
        'TGT', 'GD', 'AEP', 'D', 'SRE', 'PH', 'MCHP', 'WELL', 'A', 'EW',
        'CARR', 'OTIS', 'CTAS', 'WM', 'YUM', 'SBUX', 'NKE', 'DIS', 'PYPL', 'NOW',
    ]
