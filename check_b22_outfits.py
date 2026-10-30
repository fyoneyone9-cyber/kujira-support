import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc22 = scripts[22]
lines = sc22.split('\n')
l = lines[152]
print("Line 153 length:", len(l))
print("End:", repr(l[-50:]))
d = 0
for c in l:
    if c == '[': d += 1
    elif c == ']': d -= 1
print("Bracket balance:", d)
