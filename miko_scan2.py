# -*- coding: utf-8 -*-
# 調査: miko s1キャラ1体の定義全文を抽出して構造確認
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8').read()

def extract(cid):
    i = s.find("id: '" + cid + "'")
    if i < 0:
        i = s.find('id:"' + cid + '"')
    if i < 0:
        return None, None
    # push( の開始を後方検索
    start = s.rfind('push(', max(0, i - 500), i)
    if start < 0:
        start = i - 200
    # 対応括弧で終端を探す（簡易: 次の '});' ）
    end = s.find('});', i)
    return i, s[max(0,start-30):end+3]

for cid in ['char_miko_s1_youjo_a', 'char_miko_s2_youjo_a']:
    pos, txt = extract(cid)
    print('='*40, cid, 'pos=', pos)
    print(txt[:4000] if txt else 'NOT FOUND')
