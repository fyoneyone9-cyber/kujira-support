import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard_backup_20261020_074027.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc17 = scripts[17]

# block17の65060 (}, の行) まで深度追跡
chunk = '\n'.join(sc17.split('\n')[:65059])
depth = 0; in_str = False; sc_c = None; i = 0; last_open = []
while i < len(chunk):
    c = chunk[i]
    if in_str:
        if c == '\\': i += 2; continue
        if c == sc_c: in_str = False
    else:
        if c in ('"', "'"): in_str = True; sc_c = c
        elif c in ('(', '[', '{'):
            depth += 1
            last_open.append((depth, c, chunk[max(0,i-30):i+30]))
        elif c in (')', ']', '}'):
            depth -= 1
            if last_open: last_open.pop()
    i += 1
print(f"Depth before line 65060: {depth}")
print("Last 5 open brackets:")
for d, c, ctx in last_open[-5:]:
    print(f"  depth={d} char='{c}' ctx={repr(ctx[:60])}")
