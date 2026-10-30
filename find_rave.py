# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 合法レイブ国家 関連を探す
hits = [(m.start(), c[m.start():m.start()+300]) for m in re.finditer(r'rave|reib|レイブ|合法', c)]
for pos, h in hits[:10]:
    print(f'pos={pos}: {h[:200]}')
    print()
