from sp500 import get_all_tickers
from signals import get_data, golden_cross, death_cross, market_is_bullish
from emailer import send_email


def run():
    print('=== S&P 500 + NASDAQ Signal Bot ===')
    print('Checking market trend (SPY)...')
    bullish = market_is_bullish()
    print(f'Market bullish: {bullish}')

    print('Fetching S&P 500 + NASDAQ-100 tickers...')
    tickers = get_all_tickers()
    print(f'Total unique tickers to scan: {len(tickers)}')

    golden_crosses = []
    death_crosses = []
    errors = []

    for i, ticker in enumerate(tickers):
        try:
            df = get_data(ticker)
            if df.empty:
                continue

            if golden_cross(df):
                golden_crosses.append(ticker)
                print(f'  [GOLDEN CROSS] {ticker}')
            elif death_cross(df):
                death_crosses.append(ticker)
                print(f'  [DEATH CROSS]  {ticker}')

        except Exception as e:
            errors.append(f'{ticker}: {e}')
            continue

        if (i + 1) % 50 == 0:
            print(f'  Progress: {i + 1}/{len(tickers)} scanned')

    print(f'')
    print(f'=== Scan Complete ===')
    print(f'Golden Cross: {len(golden_crosses)}')
    print(f'Death Cross:  {len(death_crosses)}')
    print(f'Errors:       {len(errors)}')
    send_email(golden_crosses, death_crosses, bullish)


if __name__ == '__main__':
    run()
