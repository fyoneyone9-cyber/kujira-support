import re, sys, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

lines = content.split('\n')
l = lines[430544]  # usagi

# outfitsを抽出
m = re.search(r'"outfits":\s*(\[.+\])', l)
if m:
    try:
        outfits = json.loads(m.group(1))
        print(f"usagi outfits: {len(outfits)} scenes")
        for i, o in enumerate(outfits):
            print(f"  {i+1}. {o.get('label','?')[:60]}")
    except Exception as e:
        print("parse error:", e)
        print(repr(m.group(1)[:200]))
else:
    # outfitsキーを別形式で探す
    m2 = re.search(r"'outfits':\s*(\[.+\])", l)
    if m2:
        print("found with single quotes")
    else:
        print("outfits not found in line")
        print("Line sample:", repr(l[:200]))
