import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

target = content[985000:1010000]
# outfit または outfitValue キーを探す
for pat in [r"outfit\s*:", r"outfitValue\s*:", r"outfit_prompt\s*:", r"_outfitPrompt"]:
    hits = [m.start() for m in re.finditer(pat, target)]
    print(f"'{pat}' hits: {len(hits)}")
    for pos in hits[:3]:
        print(f"  abs={985000+pos}: {target[pos:pos+100].strip()}")
