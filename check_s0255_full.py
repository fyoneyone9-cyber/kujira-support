import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open('C:/AI/ComfyUI/outfit_sets.json', encoding='utf-8') as f:
    d = json.load(f)
s = d['S0255']
for i, item in enumerate(s):
    lbl = item.get('label','')
    prm = item.get('prompt','')[:60]
    print(f'{i:02d}: {lbl} | {prm}')
