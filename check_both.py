import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

sc17 = scripts[17].group(1).split('\n')
print('Block17 65055-65068:')
for j in range(65054, 65070):
    if j < len(sc17): print(j+1, repr(sc17[j][:120]))

sc22 = scripts[22].group(1).split('\n')
print('\nBlock22 378-390:')
for j in range(377, 392):
    if j < len(sc22): print(j+1, repr(sc22[j][:120]))
