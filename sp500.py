import io

def get_all_tickers():
    """Return combined S&P 500 + NASDAQ 100 tickers, deduplicated."""
    sp500 = _get_sp500_from_wikipedia()
    nasdaq100 = _get_nasdaq100_from_wikipedia()
    combined = list(dict.fromkeys(sp500 + nasdaq100))  # deduplicate, preserve order
    print(f'Tickers loaded: {len(sp500)} S&P500 + {len(nasdaq100)} NASDAQ100 = {len(combined)} unique')
    return combined


# Keep old name as alias for backward compat
def get_sp500_tickers():
    return get_all_tickers()


def _get_sp500_from_wikipedia():
    """Fetch S&P 500 tickers from Wikipedia with fallback."""
    try:
        import requests
        import pandas as pd
        url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        df = pd.read_html(io.StringIO(resp.text))[0]
        tickers = [t.replace('.', '-') for t in df['Symbol'].tolist()]
        print(f'S&P 500: loaded {len(tickers)} from Wikipedia')
        return tickers
    except Exception as e:
        print(f'S&P 500 Wikipedia failed ({e}), using fallback')
        return _sp500_fallback()


def _get_nasdaq100_from_wikipedia():
    """Fetch NASDAQ-100 tickers from Wikipedia with fallback."""
    try:
        import requests
        import pandas as pd
        url = 'https://en.wikipedia.org/wiki/Nasdaq-100'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'}
        resp = requests.get(url, headers=headers, timeout=15)
        resp.raise_for_status()
        tables = pd.read_html(io.StringIO(resp.text))
        # Find the table with 'Ticker' or 'Symbol' column
        for t in tables:
            cols = [c.lower() for c in t.columns]
            if 'ticker' in cols or 'symbol' in cols:
                col = 'Ticker' if 'Ticker' in t.columns else 'Symbol'
                tickers = [s.replace('.', '-') for s in t[col].tolist()]
                print(f'NASDAQ-100: loaded {len(tickers)} from Wikipedia')
                return tickers
        raise ValueError('No ticker table found')
    except Exception as e:
        print(f'NASDAQ-100 Wikipedia failed ({e}), using fallback')
        return _nasdaq100_fallback()


def _sp500_fallback():
    """Core S&P 500 tickers - hardcoded fallback."""
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


def _nasdaq100_fallback():
    """NASDAQ-100 tickers - hardcoded fallback."""
    return [
        'AAPL', 'MSFT', 'NVDA', 'AMZN', 'META', 'TSLA', 'GOOGL', 'GOOG', 'AVGO', 'COST',
        'NFLX', 'TMUS', 'AMD', 'QCOM', 'INTU', 'AMAT', 'ISRG', 'CSCO', 'TXN', 'BKNG',
        'AMGN', 'ADP', 'VRTX', 'MU', 'PANW', 'ADI', 'REGN', 'KLAC', 'LRCX', 'MELI',
        'MDLZ', 'GILD', 'CTAS', 'SNPS', 'CDNS', 'SBUX', 'MCHP', 'PYPL', 'CRWD', 'ABNB',
        'MAR', 'ORLY', 'WDAY', 'PCAR', 'ADSK', 'FTNT', 'MNST', 'CHTR', 'DXCM', 'ROST',
        'KDP', 'CEG', 'CPRT', 'PAYX', 'ODFL', 'FAST', 'VRSK', 'IDXX', 'EA', 'GEHC',
        'KHC', 'EXC', 'XEL', 'ON', 'CTSH', 'CCEP', 'CDW', 'FANG', 'BIIB', 'TEAM',
        'DDOG', 'ZS', 'TTD', 'ANSS', 'DLTR', 'WBD', 'ILMN', 'GFS', 'MDB', 'ALGN',
        'SMCI', 'ARM', 'APP', 'COIN', 'PLTR', 'HOOD', 'RBLX', 'MSTR', 'DUOL', 'RIVN',
        'LCID', 'NXPI', 'LULU', 'SIRI', 'WBA', 'OKTA', 'ZM', 'DOCU', 'ROKU', 'INTC',
    ]
