import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# generateSinglePanel 関数定義を探す
hits = [m.start() for m in re.finditer(r'function generateSinglePanel|generateSinglePanel\s*=\s*function|generateSinglePanel\s*=\s*async', content)]
print(f"generateSinglePanel def hits: {len(hits)}, positions: {hits[:3]}")
for pos in hits[:2]:
    print(content[pos:pos+500])
    print("---")
