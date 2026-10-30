# outfits_ref 解決ロジックとレジストリの実体を探す
import re, io
p = r'C:\AI\ComfyUI\dashboard.html'
s = io.open(p, 'r', encoding='utf-8').read()
# where is outfits_ref read (resolver)?
for m in list(re.finditer(r'outfits_ref', s))[:1]:
    pass
# find resolver code: ".outfits_ref" usage in JS logic
ms = [m.start() for m in re.finditer(r'\.outfits_ref|\[.outfits_ref.\]|outfits_ref\]', s)]
print('resolver hits', len(ms), ms[:10])
for st in ms[:5]:
    print('---', st, '---')
    print(s[st-300:st+300])
# find registry definition: maybe window.OUTFITS_DB = { S0612: [...] }
for pat in ['OUTFITS_DB', 'OUTFIT_REFS', 'REF_OUTFITS', '"S06', "'S06"]:
    ms2 = [m.start() for m in re.finditer(re.escape(pat), s)]
    print(pat, len(ms2), ms2[:8])
