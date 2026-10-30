import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17]
inner = sc17.group(1)
lines = inner.split('\n')

# 65048行から前を探す
for j in range(65049, 65020, -1):
    print(j+1, repr(lines[j][:120]))
