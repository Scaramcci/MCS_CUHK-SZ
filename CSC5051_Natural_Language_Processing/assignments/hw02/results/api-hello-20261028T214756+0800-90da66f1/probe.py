"""Single explicitly authorized hello request; no retries and no secret logging."""
import datetime
import hashlib
import json
from pathlib import Path
import platform
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main():
    root = Path(sys.argv[1]).resolve()
    values = {}
    for line in (root / '.env').read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or '=' not in line:
            continue
        name, value = line.split('=', 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        values[name.strip()] = value
    key = values.get('DEEPSEEK_API_KEY', '')
    base = values.get('DEEPSEEK_BASE_URL', '').rstrip('/')
    model = values.get('DEEPSEEK_MODEL', '')
    url = base if base.endswith('/chat/completions') else base + '/chat/completions'
    parsed = urllib.parse.urlsplit(url)
    if not key or not model or parsed.scheme != 'https' or parsed.hostname != 'ark.cn-beijing.volces.com' or parsed.username or parsed.password or parsed.query or parsed.fragment:
        print('Configuration validation failed; no request sent.')
        return 2
    def redact(text):
        return text.replace(key, '[REDACTED]')
    stamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
    run_id = 'api-hello-' + stamp.strftime('%Y%m%dT%H%M%S%z') + '-' + uuid.uuid4().hex[:8]
    evidence = root / 'results' / run_id
    evidence.mkdir(parents=True, exist_ok=False)
    script = Path(__file__).read_bytes()
    (evidence / 'probe.py').write_bytes(script)
    body = {'model': model, 'messages': [{'role': 'user', 'content': 'hello'}], 'max_tokens': 128, 'stream': False}
    result = {
        'executor': '/root (one-shot diagnostic, not independent assignment verification)',
        'authorization': 'User requested exactly one real hello API connectivity test.',
        'started_at': stamp.isoformat(), 'python': platform.python_version(),
        'command': 'python3 probe.py <hw02-directory>',
        'script_sha256': hashlib.sha256(script).hexdigest(),
        'endpoint': url, 'request': body, 'timeout_seconds': 45,
        'automatic_retries': 0, 'http_attempts': 1,
        'pricing_checked': False, 'cost': None,
    }
    # Evidence is persisted before the only HTTP attempt. Never save request headers.
    (evidence / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    request = urllib.request.Request(url, data=json.dumps(body).encode(), headers={'Content-Type': 'application/json', 'Authorization': 'Bearer ' + key}, method='POST')
    opener = urllib.request.build_opener(NoRedirect(), urllib.request.HTTPSHandler(context=ssl.create_default_context()))
    start = time.monotonic()
    exit_code = 1
    try:
        with opener.open(request, timeout=45) as response:
            raw = response.read()
            result['http_status'] = response.status
        safe_raw = redact(raw.decode('utf-8', errors='replace'))
        raw_dir = root / 'results' / 'raw' / run_id
        raw_dir.mkdir(parents=True, exist_ok=False)
        (raw_dir / 'response.json').write_text(safe_raw, encoding='utf-8')
        result['raw_response_path'] = str((raw_dir / 'response.json').relative_to(root))
        result['raw_response_sha256'] = hashlib.sha256(safe_raw.encode()).hexdigest()
        parsed_response = json.loads(safe_raw)
        choice = (parsed_response.get('choices') or [{}])[0]
        result.update({'response_model': parsed_response.get('model'), 'response_id': parsed_response.get('id'), 'reply': choice.get('message', {}).get('content'), 'finish_reason': choice.get('finish_reason'), 'usage': parsed_response.get('usage')})
        result['success'] = bool(result['reply']) and 200 <= result['http_status'] < 300
        result['status'] = 'received_reply' if result['success'] else 'response_without_answer'
        exit_code = 0 if result['success'] else 1
    except urllib.error.HTTPError as error:
        result.update({'success': False, 'status': 'http_error', 'http_status': error.code, 'error_body': redact(error.read().decode('utf-8', errors='replace'))[:2000]})
    except Exception as error:
        result.update({'success': False, 'status': 'request_failed', 'error_type': type(error).__name__, 'error': redact(str(error))[:1000]})
    result['elapsed_seconds'] = round(time.monotonic() - start, 3)
    result['exit_code'] = exit_code
    result['evidence_path'] = str((evidence / 'result.json').relative_to(root))
    safe_result = redact(json.dumps(result, ensure_ascii=False, indent=2))
    (evidence / 'result.json').write_text(safe_result, encoding='utf-8')
    print(safe_result)
    return exit_code


if __name__ == '__main__':
    raise SystemExit(main())
