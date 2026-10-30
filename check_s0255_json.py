import json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

# outfit_sets.jsonのパスを探す
candidates = [
    r'C:\AI\ComfyUI\web\outfit_sets.json',
    r'C:\AI\ComfyUI\outfit_sets.json',
]
for p in candidates:
    if os.path.exists(p):
        print(f"Found: {p}")
        with open(p, encoding='utf-8') as f:
            data = json.load(f)
        keys = list(data.keys())
        print(f"Total keys: {len(keys)}")
        print(f"S0255 exists: {'S0255' in data}")
        if 'S0255' in data:
            items = data['S0255']
            print(f"S0255 outfit count: {len(items)}")
            for i, item in enumerate(items[:5]):
                print(f"  [{i}] label={item.get('label','')} prompt={str(item.get('prompt',''))[:80]}")
        break
else:
    print("outfit_sets.json not found in candidates")
    # 検索
    for root, dirs, files in os.walk(r'C:\AI\ComfyUI'):
        for fn in files:
            if fn == 'outfit_sets.json':
                print(f"Found at: {os.path.join(root,fn)}")
