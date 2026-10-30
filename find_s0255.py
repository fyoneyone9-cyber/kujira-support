import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find("'S0255'")
if idx < 0:
    idx = content.find('"S0255"')
print(f"S0255 ref at: {idx}")

# S0255のoutfits定義を探す
idx2 = content.find("S0255")
while idx2 >= 0:
    chunk = content[idx2:idx2+200]
    if 'outfits' in chunk.lower() and 'label' in chunk.lower():
        print(f"\n--- def at {idx2} ---")
        print(content[idx2:idx2+500])
        break
    idx2 = content.find("S0255", idx2+1)

# OUTFIT_SETS or OUTFITS_REF定義を探す
hits = [m.start() for m in re.finditer(r'S0255', content)]
print(f"\nAll S0255 positions: {hits[:10]}")
