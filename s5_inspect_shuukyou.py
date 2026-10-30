import re, json, collections
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
sets = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
refs = collections.defaultdict(set)
for m in re.finditer(r"id:\s*'(char_shuukyou_[^']+)'", s):
    cid = m.group(1)
    block = s[m.start():m.start()+5000]
    rm = re.search(r'outfits_ref\s*:\s*"([^"]+)"', block)
    se = re.search(r'_s(\d+)(?:_|$)', cid)
    refs[int(se.group(1)) if se else 0].add(rm.group(1) if rm else 'NONE:'+cid)
for k in sorted(refs):
    print(k, sorted(refs[k]))
r = sorted(refs[1])[0]
v = sets[r]
items = v.get('items', v.get('outfits')) if isinstance(v, dict) else v
print('n_items=', len(items))
for it in items[:3]:
    print(json.dumps(it, ensure_ascii=False)[:500])
