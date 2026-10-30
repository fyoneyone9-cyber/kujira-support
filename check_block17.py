import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17]
inner = sc17.group(1)
lines = inner.split('\n')
print('Block17 total lines:', len(lines))
# 65055-65065
print('Around 65058:')
for j in range(65050, 65068):
    if j < len(lines): print(j+1, repr(lines[j][:130]))
# kiroku検索
for j, l in enumerate(lines):
    if 'kiroku' in l.lower():
        print('kiroku at block17 line', j+1, ':', repr(l[:80]))
        if j > 65040: break
