import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S0091 の内容確認（JKが使っているref）
idx_s91 = content.find("'S0091'")
if idx_s91 < 0: idx_s91 = content.find('"S0091"')
print(f'S0091 pos={idx_s91}')
print(content[idx_s91:idx_s91+300])
print()

# JK_Aのoutfitsブロックをそのまま取得（inline）
# char_rape_jk_B/C/D等が参照しているS0091の実体を探す
# S0091 は genref として定義されているはず
idx_s91_def = content.find('S0091')
while idx_s91_def >= 0:
    snippet = content[idx_s91_def-50:idx_s91_def+100]
    if 'outfits' in snippet.lower() or 'label' in snippet.lower():
        print(f'S0091 def at {idx_s91_def}:')
        print(snippet)
        print()
    idx_s91_def = content.find('S0091', idx_s91_def+1)
    if idx_s91_def > 20000000: break
