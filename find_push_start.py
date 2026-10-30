import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17_inner = scripts[17].group(1)
lines = sc17_inner.split('\n')

# 65060から前へ、push([ または push({ を探す（広い範囲）
for j in range(65059, 63000, -1):
    l = lines[j]
    if re.search(r'CHAR_TEMPLATES\.(female|male)\.push\(', l):
        print(f'push at line {j+1}:', repr(l[:100]))
        break
else:
    print("Not found in 63000-65059")
