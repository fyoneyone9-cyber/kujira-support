import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# 64908 の bare { 付近
print("Lines 64895-64915:")
for j in range(64894, 64916):
    if j < len(lines): print(j+1, repr(lines[j][:100]))
