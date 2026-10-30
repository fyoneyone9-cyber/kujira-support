# 目的: outfits_ref "S0273" の定義場所と構造を確認
import re, sys
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8', errors='ignore').read()
key = sys.argv[1] if len(sys.argv) > 1 else 'S0273'
out = []
for m in re.finditer(re.escape(key), s):
    i = m.start()
    ctx = s[i-120:i+80].replace('\n', '\\n')
    out.append(f'{i}: {ctx}')
open(r'C:\GensparkClaw\kujira-support\_sample_out.txt','w',encoding='utf-8').write('\n\n'.join(out[:40]) + f'\n\ntotal={len(out)}')
