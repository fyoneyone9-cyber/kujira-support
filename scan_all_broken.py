import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
broken = [(m.start(), content[m.start():m.start()+80]) for m in re.finditer(r"\},\n\{\n  id:'char_", content)]
print("All broken patterns:", len(broken))
for pos, txt in broken[:20]:
    print(" ", pos, repr(txt[:70]))
