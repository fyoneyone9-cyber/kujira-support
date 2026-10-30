import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# outfits_ref の解決ロジックを探す
hits = [m.start() for m in re.finditer(r'outfits_ref', content)]
print(f"outfits_ref hits: {len(hits)}")
for pos in hits[:8]:
    chunk = content[pos:pos+200]
    if 'resolve' in chunk.lower() or '==' in chunk or 'OUTFIT' in chunk or '[' in chunk[:50]:
        print(f"\n--- abs={pos} ---")
        print(chunk)
