import re, sys, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc22_inner = scripts[22].group(1)

tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
tmp.write(sc22_inner); tmp.close()
r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=15)
err = r.stderr.decode('utf-8', errors='replace') if r.stderr else ''
print("Block22 error:", err[:300])
# エラー行を取得
m = re.search(r':(\d+)\n', err)
if m:
    eline = int(m.group(1))
    lines = sc22_inner.split('\n')
    print(f"\nLines {eline-8} to {eline+3}:")
    for j in range(max(0,eline-9), min(len(lines), eline+4)):
        print(j+1, repr(lines[j][:120]))
os.unlink(tmp.name)
