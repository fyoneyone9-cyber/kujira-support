import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find("char_kaizo_nichijou4_aerith")
if idx < 0:
    print("Not found")
else:
    print(f"Found at {idx}")
    chunk = content[idx:idx+3000]
    print(chunk)
