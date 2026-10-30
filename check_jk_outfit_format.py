import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S0091 refの実体を探す（genref定義）
# window.CHAR_TEMPLATES_REFS や window._OUTFIT_REFS 等
for kw in ['S0091', 'CHAR_TEMPLATES_REFS', '_OUTFIT_REFS', 'outfitRefs', 'genref']:
    idx = content.find(kw)
    if idx > 0:
        print(f'=== {kw} at {idx} ===')
        print(content[idx:idx+300])
        print()
