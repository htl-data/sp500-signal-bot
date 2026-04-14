import smtplib
import os
from datetime import date
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sepa_strong, sepa_moderate, market_bullish):
    sender = os.environ['EMAIL_USER']
    password = os.environ['EMAIL_PASS']
    receiver = os.environ['EMAIL_TO']
    today = date.today().strftime('%Y-%m-%d')
    
    bullish_label = 'BULLISH' if market_bullish else 'BEARISH'
    market_color = '#27ae60' if market_bullish else '#e74c3c'
    strong_count = len(sepa_strong)
    moderate_count = len(sepa_moderate)
    
    def stock_rows_html(stocks, tier_color):
        if not stocks:
            return '<tr><td colspan="7" style="color:#888;padding:8px;text-align:center">None</td></tr>'
        rows = ''
        for s in stocks:
            ticker = s['ticker']
            sepa = s['sepa_score']
            vcp = s['vcp_score']
            rsi = s['rsi']
            low52 = s['pct_above_low52']
            high52 = s['pct_from_high52']
            vol_dry = '✓' if s['vol_dry'] else ''
            tight = '✓' if s['tight'] else ''
            rows += f'''
            <tr style="background:#f9f9f9">
                <td style="padding:8px;font-weight:bold;color:{tier_color}"><a href="https://finance.yahoo.com/quote/{ticker}" style="color:{tier_color};text-decoration:none">{ticker}</a></td>
                <td style="padding:8px;text-align:center">{sepa}/7</td>
                <td style="padding:8px;text-align:center">{vcp}/2</td>
                <td style="padding:8px;text-align:center">{rsi}</td>
                <td style="padding:8px;text-align:center">{low52}%</td>
                <td style="padding:8px;text-align:center">{high52}%</td>
                <td style="padding:8px;text-align:center">{vol_dry} {tight}</td>
            </tr>
            '''
        return rows
    
    html = f'''
    <html><body style="font-family:Arial,sans-serif;max-width:800px;margin:auto;background:#f9f9f9;padding:20px">
    <div style="background:#1a1a2e;color:#fff;padding:20px;border-radius:8px 8px 0 0;text-align:center">
        <h2 style="margin:0">SEPA Stock Scanner Report</h2>
        <p style="margin:4px 0;opacity:0.8">{today}</p>
        <p style="margin:4px 0;font-size:14px;opacity:0.7">Mark Minervini SEPA + VCP Strategy</p>
    </div>
    <div style="background:#fff;padding:20px;border:1px solid #ddd">
        <p style="font-size:15px">Market Trend (SPY): <strong style="color:{market_color}">{bullish_label}</strong></p>
        <table style="width:100%;border-collapse:collapse;margin-bottom:16px">
            <tr style="background:#d5f4e6">
                <td style="padding:10px">SEPA Strong (6/7+ trend + VCP)</td>
                <td style="padding:10px;font-size:20px;font-weight:bold;color:#27ae60;text-align:right">{strong_count}</td>
            </tr>
            <tr style="background:#fff3cd">
                <td style="padding:10px">SEPA Moderate (5/7+ trend)</td>
                <td style="padding:10px;font-size:20px;font-weight:bold;color:#f39c12;text-align:right">{moderate_count}</td>
            </tr>
        </table>

        <h3 style="color:#27ae60;border-bottom:2px solid #27ae60;padding-bottom:6px">SEPA Strong Candidates</h3>
        <table style="width:100%;border-collapse:collapse;margin-bottom:20px">
            <tr style="background:#e8f5e9;font-weight:bold;font-size:12px">
                <th style="padding:8px;text-align:left">Ticker</th>
                <th style="padding:8px;text-align:center">SEPA</th>
                <th style="padding:8px;text-align:center">VCP</th>
                <th style="padding:8px;text-align:center">RSI</th>
                <th style="padding:8px;text-align:center">+Low52</th>
                <th style="padding:8px;text-align:center">-High52</th>
                <th style="padding:8px;text-align:center">Vol Tight</th>
            </tr>
            {stock_rows_html(sepa_strong, '#27ae60')}
        </table>

        <h3 style="color:#f39c12;border-bottom:2px solid #f39c12;padding-bottom:6px">SEPA Moderate</h3>
        <table style="width:100%;border-collapse:collapse">
            <tr style="background:#fff8e1;font-weight:bold;font-size:12px">
                <th style="padding:8px;text-align:left">Ticker</th>
                <th style="padding:8px;text-align:center">SEPA</th>
                <th style="padding:8px;text-align:center">VCP</th>
                <th style="padding:8px;text-align:center">RSI</th>
                <th style="padding:8px;text-align:center">+Low52</th>
                <th style="padding:8px;text-align:center">-High52</th>
                <th style="padding:8px;text-align:center">Vol Tight</th>
            </tr>
            {stock_rows_html(sepa_moderate, '#f39c12')}
        </table>
    </div>
    <div style="background:#eee;padding:12px;text-align:center;font-size:11px;color:#888;border-radius:0 0 8px 8px">
        SEPA Criteria: MA50>MA150>MA200, MA200 up, Price>30% above 52w low, Price within 25% of 52w high<br>
        VCP: Volume dry-up + Price tightness | Universe: S&P500 + NASDAQ100
    </div>
    </body></html>
    '''
    
    plain_text = f'''SEPA Stock Scanner Report - {today}\nMarket: {bullish_label}\n\nSEPA Strong: {strong_count}\n'''
    for s in sepa_strong:
        plain_text += f"  {s['ticker']} | SEPA:{s['sepa_score']}/7 VCP:{s['vcp_score']}/2 RSI:{s['rsi']}\n"
    plain_text += f"\nSEPA Moderate: {moderate_count}\n"
    for s in sepa_moderate:
        plain_text += f"  {s['ticker']} | SEPA:{s['sepa_score']}/7\n"
    
    subject = f'[SEPA Scanner] {today} | Strong:{strong_count} Mod:{moderate_count} | {bullish_label}'
    
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText(plain_text, 'plain'))
    msg.attach(MIMEText(html, 'html'))
    
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)
    print(f'Email sent: {strong_count} SEPA strong, {moderate_count} moderate signals.')
