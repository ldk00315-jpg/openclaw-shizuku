#!/usr/bin/env python3
"""
OpenClaw API Quota Checker
Reads configured models from openclaw.json and checks each provider.
"""

import json
import os
import sys
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from pathlib import Path

OPENCLAW_DIR = Path.home() / '.openclaw'
CONFIG_FILE = OPENCLAW_DIR / 'openclaw.json'
AUTH_FILE = OPENCLAW_DIR / 'agents' / 'main' / 'agent' / 'auth-profiles.json'
UA = 'openclaw-quota-check/1.0'


def load_config():
    cfg = {}
    try:
        with open(CONFIG_FILE) as f:
            cfg = json.load(f)
    except Exception:
        pass

    auth_profiles = {}
    try:
        with open(AUTH_FILE) as f:
            auth = json.load(f)
        auth_profiles = auth.get('profiles', {})
    except Exception:
        pass

    return cfg, auth_profiles


def get_api_key(provider, cfg, auth_profiles):
    cfg_env = cfg.get('env', {})
    providers = cfg.get('models', {}).get('providers', {})

    if provider == 'groq':
        return (os.environ.get('GROQ_API_KEY')
                or providers.get('groq', {}).get('apiKey')
                or cfg_env.get('GROQ_API_KEY'))
    elif provider == 'google':
        return (os.environ.get('GEMINI_API_KEY')
                or cfg_env.get('GEMINI_API_KEY')
                or auth_profiles.get('google:default', {}).get('key'))
    elif provider == 'mistral':
        return (os.environ.get('MISTRAL_API_KEY')
                or cfg_env.get('MISTRAL_API_KEY'))
    elif provider == 'openrouter':
        return (os.environ.get('OPENROUTER_API_KEY')
                or auth_profiles.get('openrouter:default', {}).get('key')
                or auth_profiles.get('openrouter:manual', {}).get('key'))
    return None


def send_request(url, headers, data=None, timeout=15):
    req = Request(url, headers=headers)
    if data is not None:
        req.data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')
    try:
        resp = urlopen(req, timeout=timeout)
        return resp.status, dict(resp.headers), resp.read().decode('utf-8', errors='replace')[:500]
    except HTTPError as e:
        try:
            body = e.read().decode('utf-8', errors='replace')[:500]
        except Exception:
            body = ''
        return e.code, dict(e.headers), body
    except URLError as e:
        return None, {}, f'Connection error: {e.reason}'
    except Exception as e:
        return None, {}, str(e)


def parse_ratelimit_headers(headers):
    info = {}
    h = {k.lower(): v for k, v in headers.items()}
    for prefix in ['x-ratelimit-', 'ratelimit-']:
        if f'{prefix}remaining-requests' in h:
            info['remaining_req'] = h[f'{prefix}remaining-requests']
        if f'{prefix}limit-requests' in h:
            info['limit_req'] = h[f'{prefix}limit-requests']
        if f'{prefix}remaining-tokens' in h:
            info['remaining_tok'] = h[f'{prefix}remaining-tokens']
        if f'{prefix}limit-tokens' in h:
            info['limit_tok'] = h[f'{prefix}limit-tokens']
        if f'{prefix}reset-requests' in h:
            info['reset'] = h[f'{prefix}reset-requests']
        elif f'{prefix}reset' in h:
            info['reset'] = h[f'{prefix}reset']
    if 'retry-after' in h:
        info['retry_after'] = h['retry-after']
    return info


def format_status(status_code, headers, body):
    lines = []
    if status_code is None:
        lines.append('  Status: CONNECTION ERROR')
        lines.append(f'  Detail: {body[:150]}')
        return '\n'.join(lines)

    rl = parse_ratelimit_headers(headers)

    if status_code == 200:
        lines.append('  Status: OK')
    elif status_code == 429:
        lines.append('  Status: RATE LIMITED')
    elif status_code in (401, 403):
        lines.append(f'  Status: AUTH ERROR ({status_code})')
    elif status_code == 413:
        lines.append('  Status: REQUEST TOO LARGE')
    elif status_code == 404:
        lines.append('  Status: MODEL NOT FOUND (404)')
    else:
        lines.append(f'  Status: ERROR ({status_code})')

    if rl.get('remaining_req') is not None:
        lines.append(f'  Requests: {rl["remaining_req"]}/{rl.get("limit_req", "?")} remaining')
    if rl.get('remaining_tok') is not None:
        lines.append(f'  Tokens: {rl["remaining_tok"]}/{rl.get("limit_tok", "?")} remaining')
    if rl.get('reset'):
        lines.append(f'  Reset: {rl["reset"]}')
    if rl.get('retry_after'):
        lines.append(f'  Retry after: {rl["retry_after"]}s')

    if status_code >= 400:
        try:
            err = json.loads(body)
            msg = (err.get('error', {}).get('message', '')
                   or err.get('message', '')
                   or err.get('error', ''))
            if isinstance(msg, str) and msg:
                lines.append(f'  Detail: {msg[:150]}')
        except Exception:
            if body:
                lines.append(f'  Detail: {body[:150]}')

    if not rl and status_code == 200:
        lines.append('  (No rate limit headers returned)')

    return '\n'.join(lines)


def check_model(provider, model, api_key):
    if provider == 'groq':
        status, headers, body = send_request(
            'https://api.groq.com/openai/v1/chat/completions',
            {'Authorization': f'Bearer {api_key}', 'User-Agent': UA},
            {'model': model, 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 1})
        return format_status(status, headers, body)

    elif provider == 'mistral':
        status, headers, body = send_request(
            'https://api.mistral.ai/v1/chat/completions',
            {'Authorization': f'Bearer {api_key}', 'User-Agent': UA},
            {'model': model, 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 1})
        return format_status(status, headers, body)

    elif provider == 'google':
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}'
        status, headers, body = send_request(
            url, {'User-Agent': UA},
            {'contents': [{'parts': [{'text': 'hi'}]}], 'generationConfig': {'maxOutputTokens': 1}})
        return format_status(status, headers, body)

    elif provider == 'openrouter':
        status, headers, body = send_request(
            'https://openrouter.ai/api/v1/chat/completions',
            {'Authorization': f'Bearer {api_key}', 'User-Agent': UA},
            {'model': model, 'messages': [{'role': 'user', 'content': 'hi'}], 'max_tokens': 1})
        return format_status(status, headers, body)

    return '  Status: unknown provider'


def parse_model_ref(model_ref):
    parts = model_ref.split('/', 1)
    if len(parts) == 2:
        provider = parts[0]
        model = parts[1]
        if provider == 'openrouter':
            return 'openrouter', model
        return provider, model
    return None, model_ref


def main():
    cfg, auth_profiles = load_config()

    defaults = cfg.get('agents', {}).get('defaults', {}).get('model', {})
    primary = defaults.get('primary', '')
    fallbacks = defaults.get('fallbacks', [])

    all_models = [primary] + fallbacks if primary else fallbacks

    print('=== OpenClaw API Quota Status ===')
    print(f'Primary: {primary}')
    print(f'Fallbacks: {", ".join(fallbacks)}')
    print()

    for model_ref in all_models:
        provider, model = parse_model_ref(model_ref)

        if not provider:
            continue

        if provider in ('openai-codex', 'openai'):
            print(f'[{model_ref}]')
            print('  Status: OAuth - cannot check via API')
            print('  Check: https://platform.openai.com/usage')
            print()
            continue

        if provider == 'qwen-portal':
            print(f'[{model_ref}]')
            print('  Status: OAuth - cannot check via API')
            print('  Check: https://portal.qwen.ai')
            print()
            continue

        api_key = get_api_key(provider, cfg, auth_profiles)
        if not api_key:
            print(f'[{model_ref}]')
            print('  Status: API key not found')
            print()
            continue

        print(f'[{model_ref}]')
        print(check_model(provider, model, api_key))
        print()


if __name__ == '__main__':
    main()
