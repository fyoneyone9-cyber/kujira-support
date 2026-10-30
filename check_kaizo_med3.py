import re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

lines = content.split('\n')

# 430545行目 (index 430544) のusagiを確認
l = lines[430544]
# outfitsの数
outfits_count = l.count('"label"')
print("usagi outfits count:", outfits_count)
print("Line length:", len(l))

# you_b (430675) も確認
l2 = lines[430674]
print("you_b outfits count:", l2.count('"label"'))
print("you_b line length:", len(l2))

# outfit_sets.json の S0163 (医療改造に使われそうなセット) を確認
import os
outfit_path = r'C:\AI\ComfyUI\outfit_sets.json'
if os.path.exists(outfit_path):
    with open(outfit_path, encoding='utf-8') as f:
        sets = json.load(f)
    # 医療改造系のセットを探す
    for key, val in list(sets.items())[:5]:
        print(f"  {key}: {len(val)} scenes")
    # キー一覧
    keys = list(sets.keys())
    print("Total outfit sets:", len(keys))
    # S02xxあたりを確認
    for k in keys:
        if k.startswith('S02') or 'med' in k.lower():
            print(f"  {k}: {len(sets[k])} scenes")
