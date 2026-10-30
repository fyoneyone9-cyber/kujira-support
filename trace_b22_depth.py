import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc22 = scripts[22]
lines = sc22.split('\n')

depth = 0; in_str = False; sc_c = None
for line_i, line in enumerate(lines[:160]):
    old_depth = depth
    for c in line:
        if in_str:
            if c == '\\': continue
            if c == sc_c: in_str = False
        else:
            if c in ('"', "'"): in_str = True; sc_c = c
            elif c in ('(','[','{'): depth += 1
            elif c in (')',']','}'): depth -= 1
    if depth != old_depth or line.strip() in ('});', '}', '{', 'window.CHAR_TEMPLATES.female.push({'):
        print(f"L{line_i+1} depth {old_depth}->{depth}: {repr(line[:80])}")
    if line_i >= 158: break
