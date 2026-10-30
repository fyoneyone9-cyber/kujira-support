import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# bodyに outfit_prompt または outfit を送っているキー定義を探す
# 989000〜1010000 あたり
target = content[985000:1010000]
# body.outfit_prompt = や outfit_prompt: _outfitPrompt の箇所
hits = [m.start() for m in re.finditer(r'outfit_prompt\s*:', target)]
print(f"outfit_prompt: hits in body region: {len(hits)}")
for pos in hits:
    abs_pos = 985000 + pos
    print(f"\n--- abs={abs_pos} ---")
    print(target[max(0,pos-100):pos+200])
