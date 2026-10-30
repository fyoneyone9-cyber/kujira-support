# 「コピーしかない」シーンセットの特定: outfits_ref / outfit_sets を調査
import re, sys, json, collections
sys.stdout.reconfigure(encoding='utf-8')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()

# outfits_ref 使用状況
refs = re.findall(r"outfits_ref\s*:\s*['\"]([^'\"]+)['\"]", s)
print('outfits_ref counts:', collections.Counter(refs))

# OUTFIT_SETS / outfit_sets 定義場所
for m in re.finditer(r'(OUTFIT_SETS|outfit_sets|OUTFIT_REF|outfitSets)\s*[=:]', s):
    print(m.start(), s[m.start():m.start()+120].replace('\n',' ')[:120])
