import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# OUTFIT_SETS['S0255'] または S0255: { の定義を探す
hits = [m.start() for m in re.finditer(r"['\"]S0255['\"]\s*[=:]|\bS0255\b\s*:", content)]
print(f"S0255 def hits: {len(hits)}")
for pos in hits[:5]:
    print(f"\n--- abs={pos} ---")
    print(content[pos:pos+300])
