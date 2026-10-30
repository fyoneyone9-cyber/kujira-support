# -*- coding: utf-8 -*-
import io, re, sys, subprocess, os
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
t = io.open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
blocks = []
for m in re.finditer(r'<script(?![^>]*src=)[^>]*>', t):
    s = m.end(); e = t.find('</script>', s)
    if e > s: blocks.append((s, e))
print('script blocks:', len(blocks))
bad = 0
for idx, (s, e) in enumerate(blocks):
    js = t[s:e]
    if not js.strip(): continue
    p = r'C:\GensparkClaw\kujira-support\_blk_tmp.js'
    io.open(p, 'w', encoding='utf-8').write(js)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode != 0:
        bad += 1
        print(f'BLOCK {idx} (len {len(js)}) FAIL:')
        print(r.stderr[:600])
print('bad blocks:', bad)
