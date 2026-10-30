import json
with open('C:/AI/ComfyUI/outfit_sets.json', encoding='utf-8') as f:
    d = json.load(f)
keys = [k for k in d if 'S05' in k or 'S0255' in k or 's5' in k.lower()]
print('S5 keys:', keys[:20])
s0255 = d.get('S0255', [])
print('S0255 items:', len(s0255))
print('total keys:', len(d))
# S4のアイテム数確認
s4_keys = [k for k in d if 'S4' in k or 'S04' in k]
print('S4 keys:', s4_keys[:10])
