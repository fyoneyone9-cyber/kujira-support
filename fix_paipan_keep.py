import sys, json
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\quality_rules\real.json'
with open(path, encoding='utf-8') as f:
    qr = json.load(f)

keep = qr['weight_budget']['keep']
add_keys = [
    'no pubic hair',
    'smooth hairless pubic area',
    'bare crotch',
    'hairless pubic',
    'pubic hair ',  # negのpubic hair強度保護
]
added = 0
for k in add_keys:
    if k not in keep:
        keep.append(k)
        print(f'Added: {k!r}')
        added += 1

if added:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(qr, f, ensure_ascii=False, indent=2)
    print(f'Saved ({added} entries added)')
else:
    print('No changes needed')
