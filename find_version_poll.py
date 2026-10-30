import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# バージョンポーリング関連
hits = re.findall(r'.{0,100}(dashboard.version|api/version|checkVersion|_dashVer|autoReload|version.*reload|reload.*version).{0,100}', content)
for h in hits[:10]:
    print(h.strip())
    print()
