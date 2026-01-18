import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import Config
from utils.logger import ScannerLogger
from utils.http_client import HttpClient
from utils.login import LoginHelper
from core.crawler import Crawler

cfg = Config(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logger = ScannerLogger(cfg)
client = HttpClient(cfg, logger)
login = LoginHelper(client, cfg, logger)
if not login.login_dvwa():
    print('login failed')
    exit(1)

url = 'http://127.0.0.1/dvwa/vulnerabilities/xss_r/'
resp = client.get(url)
if not resp:
    print('fetch failed')
    exit(1)

crawler = Crawler(client, logger, cfg)
forms = crawler.discover_forms(resp.text, getattr(resp, 'url', url))
print('forms=', forms)
# find token
token = None
for f in forms:
    for inp in f.get('inputs', []):
        if inp.get('name') == 'user_token':
            token = inp.get('value')

payload = "<script>alert('XSS')</script>"
params = {'name': payload}
if token:
    params['user_token'] = token

r2 = client.get(url, params=params)
if not r2:
    print('payload request failed')
    exit(1)

with open('reports/xss_manual.html', 'w', encoding='utf-8') as f:
    f.write(r2.text or '')

print('saved reports/xss_manual.html; contains raw payload?', payload in (r2.text or ''))
print('escaped present?', '&lt;script' in (r2.text or ''))
