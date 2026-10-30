# -*- coding: utf-8 -*-
import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8') as f:
    c = f.read()
# STYLE_PRESETS内のキーを探す
hits = [(m.start(), c[m.start():m.start()+200]) for m in re.finditer(r'aom3|majic|AOM3|Majic', c)]
for pos, h in hits[:8]:
    print(f'pos={pos}:', h[:150])
    print()
