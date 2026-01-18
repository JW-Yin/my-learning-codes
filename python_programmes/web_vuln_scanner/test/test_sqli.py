import requests, json, time
from urllib.parse import urlencode

BASE = 'http://127.0.0.1/dvwa/vulnerabilities/sqli/'

with open('..\\payloads.json') as f:
    p = json.load(f)
payloads = p.get('sql_injection', [])

session = requests.Session()

r = session.get('http://127.0.0.1/dvwa/')
soup_token = None
try:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(r.text, 'lxml')
    tok = soup.find('input', {'name': 'user_token'})
    if tok:
        soup_token = tok.get('value')
except Exception:
    pass
if soup_token:
    data = {'username': 'admin', 'password': 'password', 'user_token': soup_token, 'Login': 'Login'}
    session.post('http://127.0.0.1/dvwa/login.php', data=data)

print('Testing', BASE)
orig = session.get(BASE)
orig_len = len(orig.text)
print('Original length:', orig_len, 'status', orig.status_code)

results = []
for pl in payloads:
    param = '1' + pl if pl and pl[0].isdigit() else pl

    url = BASE + '?id=' + requests.utils.requote_uri(param)
    start = time.time()
    r = session.get(url)
    elapsed = time.time() - start
    ln = len(r.text) if r.text else 0
    issues = []
    if r.status_code != orig.status_code:
        issues.append('status_change')
    if abs(ln - orig_len) > max(50, orig_len*0.05):
        issues.append('length_change')
    if elapsed > 4.0:
        issues.append('time_delay')
    lower = (r.text or '').lower()
    for sig in ['sql syntax', 'warning: mysql', 'unclosed', 'mysql_fetch', 'syntax error', 'database error']:
        if sig in lower:
            issues.append('error_sig')
    results.append({'payload': pl, 'url': url, 'status': r.status_code, 'len': ln, 'time': round(elapsed,2), 'issues': issues})

for res in results:
    print(res)


with open('..\\reports\\sqli_test_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)

