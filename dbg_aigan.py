import re, json, collections
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
sets = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
refs = collections.defaultdict(set)
for m in re.finditer(r"\{\s*id:\s*'(char_aigan_[^']+)'", s):
    block = s[m.start():m.start()+4000]
    rm = re.search(r'outfits_ref\s*:\s*"([^"]+)"', block)
    refs[m.group(1)].add(rm.group(1) if rm else None)
import sys
out = []
for k, v in sorted(refs.items()):
    for r in v:
        ok = r in sets if r else False
        n = 0
        if ok:
            vv = sets[r]
            items = vv.get('items', vv.get('outfits', [])) if isinstance(vv, dict) else vv
            n = len(items)
        out.append(f'{k} ref={r} injson={ok} items={n}')
print('\n'.join(out[:40]))
print('total aigan chars:', len(refs))
