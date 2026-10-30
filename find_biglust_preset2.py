import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# biglustが出てくる全箇所（行単位）
lines = content.split('\n')
for i, l in enumerate(lines, 1):
    if 'biglust' in l.lower():
        print(f"L{i}: {l.strip()[:200]}")
