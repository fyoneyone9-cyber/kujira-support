import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# 64820より前を広く探す - pushがあるところ
print("Lines 64780-64830 - push/bracket lines only:")
for j in range(64779, 64831):
    l = lines[j].strip()
    if 'push' in l or l.startswith('[') or l.startswith(']') or l == '});' or l == ']);':
        print(j+1, repr(lines[j][:100]))

# さらに前
print("\n64700-64780:")
for j in range(64699, 64780):
    l = lines[j].strip()
    if 'push' in l or l == '});' or l == ']);':
        print(j+1, repr(lines[j][:100]))
