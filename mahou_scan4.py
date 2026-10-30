# -*- coding: utf-8 -*-
# B案対象の全ID実体を確定（manga_mahou/magic_youjoのクォート形式違いも確認）
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

def ids(pat):
    return sorted(set(re.findall(r"id:\s*[\"'](" + pat + r"[a-zA-Z0-9_]*)[\"']", s)))

print('manga_mahou:', len(ids(r'char_manga_mahou_')))
for x in ids(r'char_manga_mahou_'): print('  ', x)
print('magic_youjo:', len(ids(r'char_magic_youjo_')))
# occurrences raw
print('raw manga_mahou occurrences:', s.count('char_manga_mahou_'))
print('raw magic_youjo occurrences:', s.count('char_magic_youjo_'))
# tentacle 非苗床
tent = [x for x in ids(r'char_tentacle_') if not re.match(r'char_tentacle_s\d+_', x)]
print('tentacle non-naedoko:', len(tent))
for x in tent: print('  ', x)
# push形式確認（単一行 or 複数行）
for cid in ['char_mahou_shoujo_youchien_A', 'char_mahou_youjo_A', 'char_tentacle_nurse_A', 'char_mahou_youchien_A']:
    i = s.find("id:'" + cid + "'")
    if i < 0: i = s.find('id:"' + cid + '"')
    print(cid, 'ctx:', repr(s[max(0,i-80):i+40])[:150])
