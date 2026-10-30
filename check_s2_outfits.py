import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# char_rohypnol_s2_jk_A のoutfitsを取得
idx = content.find("id:'char_rohypnol_s2_jk_A'")
if idx == -1:
    print("NOT FOUND"); sys.exit(1)

end = content.find(');', idx) + 2
block = content[idx:end]

# outfits配列を取得
m = re.search(r'outfits:(\[.*\])', block, re.DOTALL)
if not m:
    print("outfits not found"); sys.exit(1)

try:
    outfits = json.loads(m.group(1))
    for i, o in enumerate(outfits):
        print(f"[{i}] label={o.get('label','?')[:50]}")
        val = o.get('value','')
        # 問題のタグがあるか
        if 'throat' in val or 'forced oral' in val or 'irrumatio' in val:
            print(f"    ⚠️ IRAMA TAG FOUND: {val[:100]}")
        else:
            print(f"    value_start={val[:60]}")
except Exception as e:
    print(f"JSON parse error: {e}")
    # 先頭だけ表示
    print(m.group(1)[:500])
