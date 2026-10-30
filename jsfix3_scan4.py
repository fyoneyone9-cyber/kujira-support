# -*- coding: utf-8 -*-
# 調査: ');' でも括弧不一致 → push( 開始側の状態を確認する
# factory配列の直前に 'push({' が開いたまま中身が消えている可能性
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
src = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
lines = src.split('\n')
i = src.find("id: 'char_factory_")
back = src[max(0,i-1200):i]
print('=== before first factory id ===')
print(repr(back[-500:]))
# factoryブロック全体の括弧バランスを見る: push開始行の行番号を特定
# 'window.CHAR_TEMPLATES.female.push({' が直前にあるか
m = list(re.finditer(r"window\.CHAR_TEMPLATES\.female\.push\(", src[:i]))
last = m[-1]
print('last push( before factory at offset', last.start(), 'line', src[:last.start()].count('\n')+1)
print(repr(src[last.start():last.start()+200]))
