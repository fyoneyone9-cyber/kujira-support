import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22_inner = scripts[22].group(1)
lines = sc22_inner.split('\n')
print("Lines 475-495:")
for j in range(474, 496):
    print(j+1, repr(lines[j][:100]))

# depth calculation for lines up to 493
chunk = '\n'.join(lines[:492])
depth = 0; in_str = False; sc_c = None
i = 0
while i < len(chunk):
    c = chunk[i]
    if in_str:
        if c == '\\': i += 2; continue
        if c == sc_c: in_str = False
    else:
        if c in ('"', "'"): in_str = True; sc_c = c
        elif c in ('(', '[', '{'): depth += 1
        elif c in (')', ']', '}'): depth -= 1
    i += 1
print(f"\nDepth before line 493: {depth}")
