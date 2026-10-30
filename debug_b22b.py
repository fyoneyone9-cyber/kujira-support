import re, sys, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22_inner = scripts[22].group(1)
lines = sc22_inner.split('\n')
eline = 493
print(f"Lines {eline-10} to {eline+3}:")
for j in range(eline-11, min(len(lines), eline+4)):
    print(j+1, repr(lines[j][:120]))
