import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc17 = scripts[17]
lines = sc17.split('\n')

# rape系キャラの前にある最後の push( を60000行まで逆検索
print("Backwards search from 65058 for any push/]) :")
found = []
for j in range(65057, max(0, 55000), -1):
    l = lines[j].strip()
    if 'push(' in l or l == ']);' or l == '});':
        found.append((j+1, repr(lines[j][:100])))
        if len(found) >= 10:
            break
for ln, txt in found:
    print(f"  {ln}: {txt}")
