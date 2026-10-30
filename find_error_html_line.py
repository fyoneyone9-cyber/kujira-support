import re, sys, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# エラーが出るブロックを特定（block17と22）
for bi in [17, 22]:
    sc = scripts[bi]
    inner = sc.group(1)
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
    tmp.write(inner); tmp.close()
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=15)
    err = r.stderr.decode('utf-8', errors='replace')
    os.unlink(tmp.name)
    if r.returncode != 0:
        m = re.search(r':(\d+)\n', err)
        if m:
            eline = int(m.group(1))
            # block内での行番号 → HTML全体での行番号
            block_start_html_line = content[:sc.start(1)].count('\n') + 1
            html_line = block_start_html_line + eline - 1
            print(f"Block {bi}: error at block-line {eline} = HTML line {html_line}")
            lines = inner.split('\n')
            for j in range(max(0,eline-4), min(len(lines),eline+3)):
                print(f"  {j+1}: {repr(lines[j][:100])}")
