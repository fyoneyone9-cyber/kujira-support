import json, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8') as f:
    data = json.load(f)
items = data['S0255']
# item index 6 (07)
for i, item in enumerate(items):
    print(f"[{i}] label={item.get('label','')} prompt={str(item.get('prompt',''))[:120]}")
