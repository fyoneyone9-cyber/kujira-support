import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# body = { ... outfit_prompt あたりを探す
# 1007692 より前のbody構築
target = content[960000:1010000]
hits = [m.start() for m in re.finditer(r'outfit_prompt', target)]
print(f"outfit_prompt in body-build region: {len(hits)}")
for pos in hits:
    print(f"\n--- offset={960000+pos} ---")
    print(target[max(0,pos-200):pos+300])
