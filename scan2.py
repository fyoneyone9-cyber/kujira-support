import re
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
for kw in ["S0273':", '"S0273":', 'OUTFITS_SHARED', 'OUTFIT_REF', 'SHARED_OUTFITS', 'outfitsRef', '_resolveOutfits', 'OUTFIT_BANK', 'OUTFIT_DB']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), s)]
    print(kw, len(idxs), idxs[:5])
