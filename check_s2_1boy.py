import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find("id:'char_rohypnol_s2_jk_A'")
end = content.find(');', idx) + 2
block = content[idx:end]
m = re.search(r'outfits:(\[.*\])', block, re.DOTALL)
outfits = json.loads(m.group(1))

for i, o in enumerate(outfits):
    val = o.get('value','')
    has_1boy = '1boy' in val or 'faceless male' in val
    print(f"[{i:02d}] {'✅1boy' if has_1boy else '❌solo'} {o['label'][:45]}")
