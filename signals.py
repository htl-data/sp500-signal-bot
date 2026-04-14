import yfinance as yf
import pandas as pd


def get_data(ticker):
    # Use 2y to ensure enough data for MA200 (needs 200+ trading days)
    df = yf.download(ticker, period='2y', interval='1d', progress=False, auto_adjust=True)
    if df.empty:
        return df
    # Flatten multi-level columns if present (yfinance >= 0.2.x)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df['MA50'] = df['Close'].rolling(50).mean()
    df['MA200'] = df['Close'].rolling(200).mean()
    df['RSI'] = compute_rsi(df['Close'])
    df['Vol20'] = df['Volume'].rolling(20).mean()
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
    """MA50 crosses above MA200 with volume + RSI confirmation."""
    if len(df) < 201:
        return False
    try:
        ma50_today = float(df['MA50'].iloc[-1])
        ma200_today = float(df['MA200'].iloc[-1])
        ma50_prev = float(df['MA50'].iloc[-2])
        ma200_prev = float(df['MA200'].iloc[-2])
        rsi = float(df['RSI'].iloc[-1])
        vol_today = float(df['Volume'].iloc[-1])
        vol20 = float(df['Vol20'].iloc[-1])
        if pd.isna(ma50_today) or pd.isna(ma200_today) or pd.isna(rsi):
            return False
        crossed = (ma50_today > ma200_today) and (ma50_prev <= ma200_prev)
        volume_ok = vol_today > vol20
        rsi_ok = 35 < rsi < 75
        return crossed and volume_ok and rsi_ok
    except Exception:
        return False


def death_cross(df):
    """MA50 crosses below MA200 with volume + RSI confirmation."""
    if len(df) < 201:
        return False
    try:
        ma50_today = float(df['MA50'].iloc[-1])
        ma200_today = float(df['MA200'].iloc[-1])
        ma50_prev = float(df['MA50'].iloc[-2])
        ma200_prev = float(df['MA200'].iloc[-2])
        rsi = float(df['RSI'].iloc[-1])
        vol_today = float(df['Volume'].iloc[-1])
        vol20 = float(df['Vol20'].iloc[-1])
        if pd.isna(ma50_today) or pd.isna(ma200_today) or pd.isna(rsi):
            return False
        crossed = (ma50_today < ma200_today) and (ma50_prev >= ma200_prev)
        volume_ok = vol_today > vol20
        rsi_ok = rsi < 65
        return crossed and volume_ok and rsi_ok
    except Exception:
        return False


def market_is_bullish():
    """Check SPY trend: True if MA50 > MA200."""
    try:
        spy = yf.download('SPY', period='2y', interval='1d', progress=False, auto_adjust=True)
        if spy.empty or len(spy) < 200:
            return True  # Default allow if data unavailable
        if isinstance(spy.columns, pd.MultiIndex):
            spy.columns = spy.columns.get_level_values(0)
        spy['MA50'] = spy['Close'].rolling(50).mean()
        spy['MA200'] = spy['Close'].rolling(200).mean()
        return float(spy['MA50'].iloc[-1]) > float(spy['MA200'].iloc[-1])
    except Exception:
        return True
