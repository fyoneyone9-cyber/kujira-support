# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8') as f:
    lines = f.readlines()

# L24686をJSとして切り出してnode --checkで検証
# まずL24686の前後含めて_GP_BIG_GENRE_MAPブロック全体を探す
target = None
for i, l in enumerate(lines):
    if '_GP_BIG_GENRE_MAP' in l and 'var ' in l:
        target = i
        print(f'MAP start: L{i+1}')
        break

if target is not None:
    # マップ終了行を探す（};で終わる）
    end = target
    for j in range(target, min(target+200, len(lines))):
        if lines[j].rstrip().endswith('};'):
            end = j
            break
    print(f'MAP end: L{end+1}')
    
    # ブロック全体をファイルに書き出す
    block = ''.join(lines[target:end+1])
    # JS変数として書き出す
    js_test = f"var _GP_BIG_GENRE_MAP = {{}};\n// test\n{block}\nconsole.log('ok');\n"
    with open(r'C:\GensparkClaw\kujira-support\test_map.js', 'w', encoding='utf-8') as f:
        f.write(block)
    print(f'Written {len(block)} chars')
    
    # 問題行周辺を表示
    for i in range(target, min(target+5, len(lines))):
        print(f'L{i+1}: {lines[i].rstrip()[:120]}')
