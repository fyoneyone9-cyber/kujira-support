# -*- coding: utf-8 -*-
# フォールバックスパンに succubus_duo が混入する原因を直接ダンプして特定
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()
m = re.search(r"id[\"']?\s*:\s*[\"']char_onsen_ol_A[\"']", s)
i = m.start()
p_st = s.rfind('CHAR_TEMPLATES.female.push(', 0, i)
p_en = s.find('});', i)
print('p_st line', s[:p_st].count('\n')+1, 'p_en line', s[:p_en].count('\n')+1, 'span', p_en-p_st)
seg = s[p_st:p_en+3]
ids = re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']", seg)
print('ids in span:', ids[:10])
# succubus出現位置
j = seg.find('char_succubus_duo_jd_A')
print('succubus at rel', j)
print(repr(seg[max(0,j-300):j+100]))
