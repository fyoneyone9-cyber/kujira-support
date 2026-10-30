# 目的: シーズン付きキャラ1体の定義全体を出力して構造確認
import re, sys
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8', errors='ignore').read()
target = sys.argv[1] if len(sys.argv) > 1 else 'char_rohypnol_s2_'
i = s.find("id: '" + target)
if i < 0:
    i = s.find('id: "' + target)
if i < 0:
    # partial
    m = re.search(r"id:\s*['\"](" + re.escape(target) + r"[^'\"]*)", s)
    i = m.start() if m else -1
    print('matched id:', m.group(1) if m else None)
print('pos', i)
open(r'C:\GensparkClaw\kujira-support\_sample_out.txt','w',encoding='utf-8').write(s[i-80:i+6000])
