import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc22 = scripts[22]
lines = sc22.split('\n')
print("Block22 430-445:")
for j in range(429, 446):
    if j < len(lines): print(j+1, repr(lines[j][:120]))
