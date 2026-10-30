import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22 = scripts_iter[22]
inner22 = sc22.group(1)
lines22 = inner22.split('\n')

# block22のdepth追跡 (153行まで)
chunk = '\n'.join(lines22[:152])
depth = 0; in_str = False; sc_c = None; i = 0
while i < len(chunk):
    c = chunk[i]
    if in_str:
        if c == '\\': i += 2; continue
        if c == sc_c: in_str = False
    else:
        if c in ('"', "'"): in_str = True; sc_c = c
        elif c in ('(','[','{'): depth += 1
        elif c in (')',']','}'): depth -= 1
    i += 1
print(f"Depth before line 153: {depth}")
print("Lines 147-158:")
for j in range(146, 159):
    if j < len(lines22): print(j+1, repr(lines22[j][:100]))

# 最初のnegative depthを探す
depth2 = 0; in_str2 = False; sc_c2 = None; i2 = 0; neg_line = None
for line_i, line in enumerate(lines22[:160]):
    for c in line:
        if in_str2:
            if c == '\\': continue
            if c == sc_c2: in_str2 = False
        else:
            if c in ('"', "'"): in_str2 = True; sc_c2 = c
            elif c in ('(','[','{'): depth2 += 1
            elif c in (')',']','}'):
                depth2 -= 1
                if depth2 < 0 and neg_line is None:
                    neg_line = line_i + 1
                    print(f"  First negative depth at line {neg_line}: {repr(line[:60])}")
