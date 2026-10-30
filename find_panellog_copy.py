import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# コピーボタン周辺を探す
idx = content.find('コピー済')
if idx == -1:
    idx = content.find('clipboard')
print(f'found at: {idx}')
# 前後200文字
print(content[max(0,idx-300):idx+300])
