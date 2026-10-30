import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

hits = [m.start() for m in re.finditer(r"generate-panel", content)]
print(f"generate-panel hits: {len(hits)}")
for pos in hits[:5]:
    chunk = content[pos:pos+1200]
    print(f"\n--- pos={pos} ---")
    print(chunk[:600])
    print("...")
