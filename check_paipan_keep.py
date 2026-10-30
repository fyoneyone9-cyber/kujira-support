import sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\quality_rules\real.json', encoding='utf-8') as f:
    qr = json.load(f)

wb = qr.get('weight_budget', {})
keep = wb.get('keep', [])
print("=== weight_budget ===")
print(f"max_weight: {wb.get('max_weight')}")
print(f"keep entries ({len(keep)}):")
for k in keep:
    if 'pubic' in k or 'paipan' in k or 'hair' in k.lower():
        print(f"  '{k}'")
print()
# keepに no pubic hair がない場合、全タグに圧縮がかかる
print("'no pubic hair' in keep:", any('no pubic hair' in k for k in keep))
