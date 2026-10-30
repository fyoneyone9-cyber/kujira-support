# -*- coding: utf-8 -*-
# 削除で push( 開始が一緒に消え、「,」から始まる残骸になった箇所を修復
import io, re, sys, subprocess
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
P = r'C:\AI\ComfyUI\dashboard.html'
t = io.open(P, encoding='utf-8').read()

# パターン: 行頭の孤立カンマ + 次の非空行が {id:'char_ → push( が消えた残骸
pat = re.compile(r"\n[ \t]*,[ \t]*\n(\s*\{id:'char_)")
hits = pat.findall(t)
print('dangling comma heads:', len(hits))
t, n = pat.subn(r"\nwindow.CHAR_TEMPLATES.female.push(\n\1", t)
print('fixed:', n)

io.open(P, 'w', encoding='utf-8').write(t)

# 再チェック: 全scriptブロック
blocks = []
for m in re.finditer(r'<script(?![^>]*src=)[^>]*>', t):
    s = m.end(); e = t.find('</script>', s)
    if e > s: blocks.append((s, e))
bad = 0
for idx, (s, e) in enumerate(blocks):
    js = t[s:e]
    if not js.strip(): continue
    p = r'C:\GensparkClaw\kujira-support\_blk_tmp.js'
    io.open(p, 'w', encoding='utf-8').write(js)
    r = subprocess.run(['node', '--check', p], capture_output=True, text=True)
    if r.returncode != 0:
        bad += 1
        print(f'BLOCK {idx} FAIL:', r.stderr.splitlines()[-4][:200] if r.stderr else '')
        print(r.stderr[:400])
print('bad blocks:', bad)
