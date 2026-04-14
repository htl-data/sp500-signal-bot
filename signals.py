import yfinance as yf
import pandas as pd


def get_data(ticker):
    df = yf.download(ticker, period='1y', interval='1d', progress=False, auto_adjust=True)
    if df.empty:
        return df
    df['MA50'] = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()
    df['RSI'] = compute_rsi(df['Close'])
    return df


def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))


def golden_cross(df):
    if len(df) < 201:
        return False
    ma50_today = df['MA50'].iloc[-1]
    ma200_today = df['MA200'].iloc[-1]
    ma50_prev = df['MA50'].iloc[-2]
    ma200_prev = df['MA200'].iloc[-2]
    volume_ok = df['Volume'].iloc[-1] > df['Volume'].rolling(20).mean().iloc[-1]
    rsi_ok = 40 < df['RSI'].iloc[-1] < 70
    return (ma50_today > ma200_today and ma50_prev <= ma200_prev
            and volume_ok and rsi_ok)


def death_cross(df):
    if len(df) < 201:
        return False
    ma50_today = df['MA50'].iloc[-1]
    ma200_today = df['MA200'].iloc[-1]
    ma50_prev = df['MA50'].iloc[-2]
    ma200_prev = df['MA200'].iloc[-2]
    volume_ok = df['Volume'].iloc[-1] > df['Volume'].rolling(20).mean().iloc[-1]
    rsi_ok = df['RSI'].iloc[-1] < 60
    return (ma50_today < ma200_today and ma50_prev >= ma200_prev
            and volume_ok and rsi_ok)


def market_is_bullish():
    """Check SPY trend - only trade longs when market is healthy."""
    spy = yf.download('SPY', period='1y', interval='1d', progress=False, auto_adjust=True)
    if spy.empty or len(spy) < 50:
        return True  # Default to allow if data unavailable
    spy['MA50'] = spy['Close'].rolling(50).mean()
    spy['MA200'] = spy['Close'].rolling(200).mean()
    return spy['MA50'].iloc[-1] > spy['MA200'].iloc[-1]
