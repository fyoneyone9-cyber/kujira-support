# -*- coding: utf-8 -*-
# dashboard.htmlの全<script>ブロックを抽出しnode --checkで構文検証
# 何をなぜ: switchTab未定義=定義元scriptブロックがSyntaxErrorで全滅の疑い。壊れたブロックを特定する
import re, sys, io, os, subprocess, tempfile
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
blocks = []
for m in re.finditer(r'<script(?:\s[^>]*)?>(.*?)</script>', s, re.DOTALL):
    body = m.group(1)
    if len(body.strip()) < 10:
        continue
    if 'src=' in m.group(0)[:100] and not body.strip():
        continue
    blocks.append((m.start(), body))
print('script blocks:', len(blocks))
tmpdir = tempfile.mkdtemp()
bad = []
for idx, (pos, body) in enumerate(blocks):
    p = os.path.join(tmpdir, f'blk{idx}.js')
    open(p, 'w', encoding='utf-8').write(body)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode != 0:
        line_in_file = s[:pos].count('\n') + 1
        bad.append((idx, pos, line_in_file, r.stderr[:500]))
for idx, pos, line, err in bad:
    print('=== BAD block', idx, 'html line', line)
    print(err)
print('bad blocks:', len(bad))
# switchTab定義がどのブロックにあるか
for idx, (pos, body) in enumerate(blocks):
    if 'function switchTab' in body or 'switchTab =' in body:
        print('switchTab defined in block', idx, 'html line', s[:pos].count('\n')+1)
