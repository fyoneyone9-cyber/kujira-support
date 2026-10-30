import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sets = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
for r in ['S0652', 'S0653', 'S0661']:
    v = sets[r]
    items = v.get('items', v.get('outfits')) if isinstance(v, dict) else v
    print('===', r, 'keys:', list(v.keys()) if isinstance(v, dict) else 'list', 'n=', len(items))
    for it in items[:2]:
        print(json.dumps(it, ensure_ascii=False)[:700])
    print('labels:', [it.get('label','')[:20] for it in items[:6]])
