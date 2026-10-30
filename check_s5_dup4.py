# outfits_ref の中身(OUTFITS_DB等)が別refでも同一コピーでないか検証
import re, collections, hashlib, json

s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()

# ref定義を探す: "S0436": [ ... ] のような形式を想定
# まず定義場所の形式を確認
m = re.search(r'["\']S0436["\']\s*[:=]', s)
print('S0436 def found:', bool(m), m.start() if m else '')
if m:
    print(repr(s[m.start()-200:m.start()+500]))
