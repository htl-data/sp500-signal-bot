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

    market_status = 'BULLISH (SPY MA50 > MA200)' if market_bullish else 'BEARISH (SPY MA50 < MA200)'

    lines = []
    lines.append(f'S&P 500 Daily Signal Report - {today}')
    lines.append(f'Market Status: {market_status}')
    lines.append('')

    if golden_crosses:
        lines.append(f'GOLDEN CROSS ({len(golden_crosses)} stocks):')
        for t in golden_crosses:
            lines.append(f'  + {t}')
    else:
        lines.append('GOLDEN CROSS: None today')

    lines.append('')

    if death_crosses:
        lines.append(f'DEATH CROSS ({len(death_crosses)} stocks):')
        for t in death_crosses:
            lines.append(f'  - {t}')
    else:
        lines.append('DEATH CROSS: None today')

    lines.append('')
    lines.append('Filters applied: Volume > 20-day avg | RSI in valid range | SPY trend check')
    lines.append('--- Automated by sp500-signal-bot ---')

    content = '\n'.join(lines)

    msg = MIMEMultipart()
    msg['Subject'] = f'S&P500 Signals {today} | GC:{len(golden_crosses)} DC:{len(death_crosses)}'
    msg['From'] = sender
    msg['To'] = receiver
    msg.attach(MIMEText(content, 'plain'))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(sender, password)
        server.send_message(msg)

    print(f'Email sent: {len(golden_crosses)} golden cross, {len(death_crosses)} death cross signals.')
