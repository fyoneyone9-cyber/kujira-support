import re, sys, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')

tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
tmp.write(sc17); tmp.close()
r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=15)
err = r.stderr.decode('utf-8', errors='replace')
print("Error:", err[:300])
m = re.search(r':(\d+)\n', err)
if m:
    eline = int(m.group(1))
    print(f"\nLines {eline-5} to {eline+2}:")
    for j in range(max(0,eline-6), min(len(lines),eline+3)):
        print(j+1, repr(lines[j][:100]))
os.unlink(tmp.name)

# depth tracking - find where it first goes negative
depth = 0; in_str = False; sc_c = None
line_num = 1; char_num = 0
first_neg = None
for i, c in enumerate(sc17):
    if c == '\n': line_num += 1; char_num = 0
    char_num += 1
    if in_str:
        if c == '\\': continue
        if c == sc_c: in_str = False
    else:
        if c in ('"', "'"): in_str = True; sc_c = c
        elif c in ('(','[','{'): depth += 1
        elif c in (')',']','}'):
            depth -= 1
            if depth < 0 and first_neg is None:
                first_neg = (line_num, char_num, c, depth)
                print(f"\nFirst negative depth at line {line_num}, char {char_num}: '{c}' depth={depth}")
                print("  Context:", repr(sc17[max(0,i-30):i+30]))
                break
