import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# block17の最初の1000行を表示（CHAR_TEMPLATES絡みのもの）
print("Block17 first 50 significant lines:")
count = 0
for j, l in enumerate(lines):
    ls = l.strip()
    if 'CHAR_TEMPLATES' in ls or ls in ('});', ']);', '[', ']') or ls.endswith('.push([') or ls.endswith('.push('):
        print(j+1, repr(l[:120]))
        count += 1
        if count >= 30: break
