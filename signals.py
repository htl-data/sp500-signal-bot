"""SEPA Strategy Scanner - Minervini Style"""
import yfinance as yf
import pandas as pd
import numpy as np

def get_data(ticker):
    try:
        df = yf.download(ticker, period='2y', interval='1d', progress=False, auto_adjust=True)
        if df.empty:
            return df
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)
        df['MA50'] = df['Close'].rolling(50).mean()
        df['MA150'] = df['Close'].rolling(150).mean()
        df['MA200'] = df['Close'].rolling(200).mean()
        df['RSI'] = compute_rsi(df['Close'])
        df['Vol20'] = df['Volume'].rolling(20).mean()
        df['Vol50'] = df['Volume'].rolling(50).mean()
        df['High52w'] = df['High'].rolling(252).max()
        df['Low52w'] = df['Low'].rolling(252).min()
        return df
    except Exception:
        return pd.DataFrame()

def compute_rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def sepa_trend_template(df):
    if len(df) < 201:
        return {'pass': False, 'score': 0}
    try:
        close = float(df['Close'].iloc[-1])
        ma50 = float(df['MA50'].iloc[-1])
        ma150 = float(df['MA150'].iloc[-1])
        ma200 = float(df['MA200'].iloc[-1])
        high52 = float(df['High52w'].iloc[-1])
        low52 = float(df['Low52w'].iloc[-1])
        ma200_20d_ago = float(df['MA200'].iloc[-21]) if len(df) > 20 else ma200
        ma200_up = ma200 > ma200_20d_ago
        pct_above_low = ((close - low52) / low52) * 100 if low52 > 0 else 0
        pct_from_high = ((high52 - close) / high52) * 100 if high52 > 0 else 100
        checks = [
            close > ma150 and close > ma200,
            ma150 > ma200,
            ma200_up,
            ma50 > ma150 and ma50 > ma200,
            close > ma50,
            pct_above_low >= 30,
            pct_from_high <= 25
        ]
        score = sum(checks)
        return {
            'pass': score >= 6,
            'score': score,
            'pct_above_low52': round(pct_above_low, 1),
            'pct_from_high52': round(pct_from_high, 1)
        }
    except Exception:
        return {'pass': False, 'score': 0}

def vcp_score(df):
    try:
        vol_recent = df['Volume'].iloc[-5:].mean()
        vol50 = float(df['Vol50'].iloc[-1])
        vol_dry = vol_recent < vol50 * 0.7
        recent_range = (df['High'].iloc[-10:].max() - df['Low'].iloc[-10:].min()) / df['Close'].iloc[-1]
        earlier_range = (df['High'].iloc[-30:-10].max() - df['Low'].iloc[-30:-10].min()) / df['Close'].iloc[-20]
        tight = recent_range < earlier_range * 0.5
        return {'vol_dry': vol_dry, 'tight': tight, 'score': int(vol_dry) + int(tight)}
    except Exception:
        return {'vol_dry': False, 'tight': False, 'score': 0}

def analyze_stock(ticker):
    df = get_data(ticker)
    if df.empty or len(df) < 201:
        return None
    trend = sepa_trend_template(df)
    vcp = vcp_score(df)
    rsi = float(df['RSI'].iloc[-1]) if not pd.isna(df['RSI'].iloc[-1]) else 50
    total_score = trend['score'] + vcp['score']
    signal_type = None
    if trend['pass'] and vcp['score'] >= 1:
        signal_type = 'SEPA_STRONG'
    elif trend['score'] >= 5:
        signal_type = 'SEPA_MODERATE'
    return {
        'ticker': ticker,
        'signal': signal_type,
        'total_score': total_score,
        'sepa_score': trend['score'],
        'vcp_score': vcp['score'],
        'rsi': round(rsi, 1),
        'pct_above_low52': trend.get('pct_above_low52', 0),
        'pct_from_high52': trend.get('pct_from_high52', 0),
        'vol_dry': vcp['vol_dry'],
        'tight': vcp['tight']
    }

def market_is_bullish():
    try:
        spy = yf.download('SPY', period='2y', interval='1d', progress=False, auto_adjust=True)
        if spy.empty or len(spy) < 200:
            return True
        if isinstance(spy.columns, pd.MultiIndex):
            spy.columns = spy.columns.get_level_values(0)
        spy['MA50'] = spy['Close'].rolling(50).mean()
        spy['MA200'] = spy['Close'].rolling(200).mean()
        return float(spy['MA50'].iloc[-1]) > float(spy['MA200'].iloc[-1])
    except Exception:
        return True
