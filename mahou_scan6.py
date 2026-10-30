# -*- coding: utf-8 -*-
# tentacle系（配列オブジェクト形式）とmahou系（複数行push形式）の正確な構造把握
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

# 1) tentacle_nurse_A の所属ブロック先頭を探す（配列リテラル内か push内か）
i = s.find("id: 'char_tentacle_nurse_A'")
blk = s[max(0,i-3000):i]
j = blk.rfind('push(')
k = blk.rfind('= [')
print('push( at', j, ' / = [ at', k, '(relative)')
print(repr(s[max(0,i-400):i+60])[-500:])
print('===')
# 2) 全24体それぞれの定義開始形式
for cid in ['char_tentacle_youjo_A','char_tentacle_shougaku_A','char_tentacle_chuugaku_A','char_tentacle_elf_A','char_tentacle_mahou_A']:
    m = re.search(r"id:\s*['\"]" + cid + r"['\"]", s)
    i2 = m.start()
    print(cid, '||', repr(s[max(0,i2-100):i2+30])[:180])
    print('---')
# 3) mahou_shoujo pushは複数行 window...push({\n id:...）で }); まで
m2 = re.search(r"window\.CHAR_TEMPLATES\.female\.push\(\{\s*\n\s*id:'char_mahou_shoujo_youchien_A'", s)
print('mahou_shoujo multiline push found:', bool(m2))
