import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# 64858より前でpushを探す
print("Lines 64820-64862:")
for j in range(64819, 64862):
    l = lines[j].strip()
    if 'push' in l or l in ('{', '[', '};', '];', '});', ']);'):
        print(j+1, repr(lines[j][:100]))
