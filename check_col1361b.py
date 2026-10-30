# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# ブラウザのJSエラーはバイト列でなくJS文字列位置（UTF-16）
# L24686を確認
l = lines[24685]
# UTF-16エンコードでの位置を計算
l_utf16 = l.encode('utf-16-le')
# col1361はcharacter index
# まずUTF-16の1361*2バイト目付近をデコード
byte_pos = 1361 * 2
print(f'UTF-16 byte {byte_pos}: {repr(l_utf16[byte_pos-10:byte_pos+20])}')

# 単純にcharacter indexとしてチェック
print(f'char[1358:1370]: {repr(l[1358:1370])}')

# さらに「:」の位置をすべてリスト
colon_positions = [i for i, c in enumerate(l) if c == ':']
# 1361周辺
near = [p for p in colon_positions if 1350 <= p <= 1380]
print(f'Colon positions near 1361: {near}')
for p in near:
    print(f'  col{p}: {repr(l[p-30:p+40])}')

# 全体でsyntaxエラーになりそうな「':」パターン（key不正）
suspects = re.findall(r"'[^']*':\s*label:", l)
print(f'Suspect patterns in L24686: {suspects}')
