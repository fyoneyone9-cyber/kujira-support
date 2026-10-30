# outfits_ref レジストリの実体を探す
import re, io
p = r'C:\AI\ComfyUI\dashboard.html'
s = io.open(p, 'r', encoding='utf-8').read()
for pat in ['OUTFITS_REF', 'outfits_ref', 'S0612', 'OUTFIT_BANK', 'outfitBank']:
    ms = [m.start() for m in re.finditer(re.escape(pat), s)]
    print(pat, len(ms), ms[:6])
# dump around first S0612 definition (not the ref usage)
ms = [m.start() for m in re.finditer(r'S0612', s)]
for st in ms[:4]:
    print('---', st, '---')
    print(s[st-200:st+600])
