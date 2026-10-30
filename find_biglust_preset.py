import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# STYLE_PRESETS内でbiglustを使っているエントリを探す
for m in re.finditer(r'[^\n]{0,200}biglust[^\n]{0,200}', content, re.IGNORECASE):
    print(m.group())
    print()
