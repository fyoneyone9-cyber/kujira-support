import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# jk_A の scene 00 の value を取得
jka = content.find("char_kakuseizai_jk_A'")
oi = content.find('outfits:[', jka)
# 最初のoutfitだけ取る
first = content.find("'label':", oi)
val_start = content.find("'value':'", first)
val_end = content.find("'}", val_start + 9)
val = content[val_start+9:val_end]
print("jk_A scene 00 value (先頭500):")
print(val[:500])
print()
# expression関連タグを抽出
expr = re.findall(r'\([^)]*(?:expression|eyes|brow|lip|teeth|daze|flushed|ラリ)[^)]*(?::[0-9.]+)?\)', val)
print("expression tags:", expr)
