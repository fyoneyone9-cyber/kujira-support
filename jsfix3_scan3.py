# -*- coding: utf-8 -*-
# 構造確認: factory配列の開始と、孤立';'の後続を確認して正しい修正を決める
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
src = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
lines = src.split('\n')
# factory_chuugaku_C の後(415315)から ';'(415362)までに何があったか → 全部空白と確認済み
# 配列/push開始を遡る: 'char_factory' 最初の出現から前方を見る
i = src.find("id: 'char_factory_")
back = src[max(0,i-2500):i]
print(repr(back[-900:]))
print('=== after ; ===')
c = sum(len(l)+1 for l in lines[:415362])  # offset after line 415362
print(repr(src[c:c+300]))
