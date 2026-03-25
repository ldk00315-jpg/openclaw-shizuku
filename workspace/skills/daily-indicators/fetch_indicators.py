#!/usr/bin/env python3
"""
Daily Indicators Fetcher
Uses curl for HTTP requests (more reliable with Yahoo Finance).
"""

import json
import subprocess
import time

SYMBOLS = [
    ('USDJPY=X', 'USD/JPY', 'fx'),
    ('CL=F', 'WTI', 'commodity'),
    ('^N225', 'Nikkei 225', 'index'),
    ('^DJI', 'Dow Jones', 'index'),
    ('^IXIC', 'NASDAQ', 'index'),
    ('^GSPC', 'S&P 500', 'index'),
]


def curl_get(url, timeout=15):
    try:
        result = subprocess.run(
            ['curl', '-s', '-m', str(timeout), '-H', 'User-Agent: Mozilla/5.0', url],
            capture_output=True, text=True, timeout=timeout+5)
        if result.returncode == 0 and result.stdout:
            return result.stdout
    except Exception:
        pass
    return None


def fetch_quote(symbol):
    url = f'https://query2.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=2d'
    body = curl_get(url)
    if not body:
        return None
    try:
        data = json.loads(body)
        err = data.get('chart', {}).get('error')
        if err:
            return None
        meta = data['chart']['result'][0]['meta']
        price = meta.get('regularMarketPrice', 0)
        prev = meta.get('chartPreviousClose', 0)
        if not prev:
            prev = meta.get('previousClose', 0)
        return price, prev
    except Exception:
        return None


def format_quote(name, qtype, price, prev):
    if prev and prev != 0:
        change = price - prev
        change_pct = (change / prev) * 100
        sign = '+' if change >= 0 else ''
    else:
        change = 0
        change_pct = 0
        sign = ''

    if qtype == 'fx':
        return f'{price:.3f} ({sign}{change:.3f}, {sign}{change_pct:.2f}%)'
    elif qtype == 'commodity':
        return f'${price:.2f} ({sign}{change:.2f}, {sign}{change_pct:.2f}%)'
    else:
        return f'{price:,.2f} ({sign}{change:,.2f}, {sign}{change_pct:.2f}%)'


def fetch_weather():
    body = curl_get('https://wttr.in/Komagane,Japan?format=j1')
    if not body:
        return 'ERROR: connection failed'
    try:
        data = json.loads(body)
        current = data.get('current_condition', [{}])[0]
        today = data.get('weather', [{}])[0]

        temp_c = current.get('temp_C', '?')
        weather_desc = ''
        desc = current.get('lang_ja', [{}])
        if desc:
            weather_desc = desc[0].get('value', '')
        if not weather_desc:
            wd = current.get('weatherDesc', [{}])
            if wd:
                weather_desc = wd[0].get('value', '')

        max_temp = today.get('maxtempC', '?')
        min_temp = today.get('mintempC', '?')

        return f'{weather_desc} / {temp_c}C (high {max_temp}C / low {min_temp}C)'
    except Exception as e:
        return f'ERROR: {str(e)[:80]}'


def main():
    print('=== Daily Indicators ===')
    print()

    print('[Market Data]')
    for symbol, name, qtype in SYMBOLS:
        result = fetch_quote(symbol)
        if result:
            price, prev = result
            print(f'  {name}: {format_quote(name, qtype, price, prev)}')
        else:
            print(f'  {name}: ERROR: data not available')
        time.sleep(0.5)
    print()

    print('[Komagane Weather]')
    weather = fetch_weather()
    print(f'  {weather}')


if __name__ == '__main__':
    main()
