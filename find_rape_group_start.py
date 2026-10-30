import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# 64828より前のpushか[ を探す
for j in range(64827, max(0, 64000), -1):
    l = lines[j].strip()
    if 'CHAR_TEMPLATES' in l and 'push' in l:
        print(f"Found CHAR push at line {j+1}: {repr(lines[j][:120])}")
        break
    if l == '[' or l.endswith('.push([') or l.endswith('.push('):
        print(f"Found bracket/push at line {j+1}: {repr(lines[j][:120])}")
        break
    if l == '});' or l == ']);':
        print(f"Found close at line {j+1}: {repr(lines[j][:80])}")
        # この閉じの次のpushを探す
        break
