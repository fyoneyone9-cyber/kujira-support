import re, sys, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17_inner = scripts[17].group(1)

tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
tmp.write(sc17_inner); tmp.close()
r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=30)
err = r.stderr.decode('utf-8', errors='replace') if r.stderr else ''
print("Block17 error:")
print(err[:500])

# エラー行の前後10行表示
m = re.search(r':(\d+)\n', err)
if m:
    eline = int(m.group(1))
    lines = sc17_inner.split('\n')
    print(f"\nAround line {eline}:")
    for j in range(max(0,eline-5), min(len(lines), eline+5)):
        print(j+1, repr(lines[j][:130]))
os.unlink(tmp.name)
