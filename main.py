import datetime
from sp500 import get_all_tickers
from signals import analyze_stock, market_is_bullish
from emailer import send_email

def run():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M UTC')
    print(f'=== S&P 500 + NASDAQ SEPA Scanner ===')
    print(f'Run time: {now}')

    print('Checking market trend (SPY)...')
    bullish = market_is_bullish()
    trend = 'BULLISH' if bullish else 'BEARISH'
    print(f'Market: {trend} (SPY MA50 vs MA200)')

    print('Fetching S&P 500 + NASDAQ-100 tickers...')
    tickers = get_all_tickers()
    print(f'Total unique tickers to scan: {len(tickers)}')

    sepa_strong = []
    sepa_moderate = []
    errors = []

    for i, ticker in enumerate(tickers):
        try:
            result = analyze_stock(ticker)
            if result is None:
                continue
            
            if result['signal'] == 'SEPA_STRONG':
                sepa_strong.append(result)
                print(f'  [SEPA STRONG] {ticker} | Score:{result["total_score"]} SEPA:{result["sepa_score"]}/7 VCP:{result["vcp_score"]}/2 RSI:{result["rsi"]}')
            elif result['signal'] == 'SEPA_MODERATE':
                sepa_moderate.append(result)
                print(f'  [SEPA MODERATE] {ticker} | Score:{result["total_score"]} SEPA:{result["sepa_score"]}/7')
        except Exception as e:
            errors.append(f'{ticker}: {e}')
            continue
        
        if (i + 1) % 50 == 0:
            print(f'  Progress: {i + 1}/{len(tickers)} scanned')

    print(f'')
    print(f'=== Scan Complete ===')
    print(f'SEPA Strong    : {len(sepa_strong)}')
    if sepa_strong:
        print(f'  Tickers: {", ".join([s["ticker"] for s in sepa_strong])}')
    print(f'SEPA Moderate  : {len(sepa_moderate)}')
    if sepa_moderate:
        print(f'  Tickers: {", ".join([s["ticker"] for s in sepa_moderate])}')
    print(f'Errors         : {len(errors)}')

    send_email(sepa_strong, sepa_moderate, bullish)

if __name__ == '__main__':
    run()
