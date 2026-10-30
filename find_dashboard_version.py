import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# バージョン番号の定義箇所
m = re.search(r'name=["\']version["\'][^>]*content=["\']([^"\']+)["\']', content)
if m:
    print('version meta:', m.group(1))
m2 = re.search(r'content=["\']([0-9]+)["\'][^>]*name=["\']version["\']', content)
if m2:
    print('version meta2:', m2.group(1))

# ダッシュボードが自分自身のURLをどう参照しているか
for pat in [r'dashboard\.html', r'location\.reload', r'version.*check', r'SW\.|serviceWorker', r'EventSource']:
    hits = re.findall(r'.{0,60}' + pat + r'.{0,60}', content)
    if hits:
        print(f'\n[{pat}]')
        for h in hits[:3]: print(' ', h.strip())
