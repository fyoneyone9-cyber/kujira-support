import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

sc17 = scripts[17].group(1).split('\n')
print('Block17 65060-65080:')
for j in range(65059, 65083):
    if j < len(sc17): print(j+1, repr(sc17[j][:100]))

sc22 = scripts[22].group(1).split('\n')
print('\nBlock22 450-465:')
for j in range(449, 465):
    if j < len(sc22): print(j+1, repr(sc22[j][:100]))
