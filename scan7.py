import json
d = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
for k in ['S0612', 'S0432', 'SS01', 'S0273']:
    v = d.get(k)
    print(k, type(v), (len(v) if hasattr(v, '__len__') else ''))
    t = json.dumps(v, ensure_ascii=False)[:500]
    open(r'C:\GensparkClaw\kujira-support\_s7_' + k + '.txt', 'w', encoding='utf-8').write(json.dumps(v, ensure_ascii=False, indent=1)[:4000])
