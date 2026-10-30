import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# rohypnol S1 キャラID一覧
ids = re.findall(r'id:\s*["\']?(char_rohypnol[^"\',\s}]+)', content)
unique = sorted(set(ids))
print('rohypnol chars:', unique)

# char_rohypnol_aerith の真のS1 outfit 17 を探す
# S1キャラはindex=17が「挿入②」のはず
idx = content.find("char_rohypnol_aerith")
# S2が先にある可能性 → S1本体（S2定義より前）を探す
# S1はS2-01より前のアウトフィットを持つはず
chunk = content[idx:idx+120000]

# 先頭30 outfits のラベルだけ出す
labels = re.findall(r'"label"\s*:\s*"([^"]+)"', chunk)
print()
print('First 30 outfit labels in char_rohypnol_aerith block:')
for i, l in enumerate(labels[:30]):
    print(f'  [{i:02d}] {l}')
