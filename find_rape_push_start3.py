import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# 64700前を広く探す
print("64400-64700 - push/bracket:")
for j in range(64399, 64700):
    l = lines[j].strip()
    if 'CHAR_TEMPLATES' in l or l == '});' or l == ']);':
        print(j+1, repr(lines[j][:100]))
