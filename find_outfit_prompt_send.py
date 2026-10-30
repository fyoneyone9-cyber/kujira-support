import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# generate-panel API呼び出しでoutfit_promptを送っているか
# fetch('/api/generate-panel' の周辺を探す
hits = [m.start() for m in re.finditer(r"generate-panel", content)]
print(f"generate-panel hits: {len(hits)}")
for pos in hits[:3]:
    chunk = content[pos:pos+800]
    if 'outfit_prompt' in chunk or 'outfit' in chunk.lower():
        print(f"\n--- pos={pos} ---")
        print(chunk[:800])
