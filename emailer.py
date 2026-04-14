import smtplib
import os
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(golden_crosses, death_crosses, market_bullish):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver = os.environ['EMAIL_TO']
    today = date.today().strftime('%Y-%m-%d')

    bullish_emoji = 'BULLISH' if market_bullish else 'BEARISH'
    market_color = '#27ae60' if market_bullish else '#e74c3c'
    gc_count = len(golden_crosses)
    dc_count = len(death_crosses)

    # ---- HTML body ----
    def ticker_rows(tickers, color, symbol):
        if not tickers:
            return '<tr><td colspan="2" style="color:#888;padding:8px">None today</td></tr>'
        rows = ''
        for t in tickers:
            rows += f'<tr><td style="padding:6px 12px;font-weight:bold;color:{color}">{symbol} {t}</td><td style="padding:6px 12px"><a href="https://finance.yahoo.com/quote/{t}" style="color:#2980b9">Yahoo Finance</a></td></tr>'
        return rows

    html = f"""
    <html><body style="font-family:Arial,sans-serif;max-width:600px;margin:auto;background:#f9f9f9;padding:20px">
    <div style="background:#1a1a2e;color:#fff;padding:20px;border-radius:8px 8px 0 0;text-align:center">
        <h2 style="margin:0">SP500 + NASDAQ Signal Report</h2>
        <p style="margin:4px 0;opacity:0.8">{today}</p>
    </div>
    <div style="background:#fff;padding:20px;border:1px solid #ddd">
        <p style="font-size:15px">Market Trend (SPY MA50 vs MA200): <strong style="color:{market_color}">{bullish_emoji}</strong></p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:16px">
            <tr style="background:#eaf4ea">
                <td style="padding:10px;font-size:14px">Golden Cross (Bullish)</td>
                <td style="padding:10px;font-size:20px;font-weight:bold;color:#27ae60;text-align:right">{gc_count}</td>
            </tr>
            <tr style="background:#fdecea">
                <td style="padding:10px;font-size:14px">Death Cross (Bearish)</td>
                <td style="padding:10px;font-size:20px;font-weight:bold;color:#e74c3c;text-align:right">{dc_count}</td>
            </tr>
        </table>

        <h3 style="color:#27ae60;border-bottom:2px solid #27ae60;padding-bottom:6px">Golden Cross Signals</h3>
        <table style="width:100%;border-collapse:collapse">
            {ticker_rows(golden_crosses, '#27ae60', '+')}
        </table>

        <h3 style="color:#e74c3c;border-bottom:2px solid #e74c3c;padding-bottom:6px;margin-top:20px">Death Cross Signals</h3>
        <table style="width:100%;border-collapse:collapse">
            {ticker_rows(death_crosses, '#e74c3c', '-')}
        </table>
    </div>
    <div style="background:#eee;padding:12px;text-align:center;font-size:11px;color:#888;border-radius:0 0 8px 8px">
        Universe: S&amp;P 500 + NASDAQ-100 (~523 tickers) | Filters: Volume &gt; 20d avg, RSI in range<br>
        Automated by <a href="https://github.com/htl-data/sp500-signal-bot">sp500-signal-bot</a>
    </div>
    </body></html>
    """

    # ---- Plain text fallback ----
    plain_lines = [
        f'S&P 500 + NASDAQ Daily Signal Report - {today}',
        f'Market Status: {bullish_emoji} (SPY MA50 vs MA200)',
        '',
        f'GOLDEN CROSS ({gc_count}):',
    ]
    for t in golden_crosses:
        plain_lines.append(f'  + {t}')
    if not golden_crosses:
        plain_lines.append('  None today')
    plain_lines.append('')
    plain_lines.append(f'DEATH CROSS ({dc_count}):')
    for t in death_crosses:
        plain_lines.append(f'  - {t}')
    if not death_crosses:
        plain_lines.append('  None today')
    plain_lines.append('')
    plain_lines.append('Universe: S&P 500 + NASDAQ-100 | github.com/htl-data/sp500-signal-bot')
    plain_text = '\n'.join(plain_lines)

    subject = f'[Signal Bot] {today} | GC:{gc_count} DC:{dc_count} | SPY:{bullish_emoji}'

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText(plain_text, 'plain'))
    msg.attach(MIMEText(html, 'html'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
    print(f'Email sent: {gc_count} golden cross, {dc_count} death cross signals.')
