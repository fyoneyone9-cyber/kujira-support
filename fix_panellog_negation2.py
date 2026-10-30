import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8') as f:
    content = f.read()

# 検索
marker = "navigator.clipboard.writeText(document.getElementById(\\'lp\\').textContent).then(function(){"
idx = content.find(marker)
print(f"idx={idx}")
if idx != -1:
    # 前後を確認
    print(repr(content[idx:idx+200]))
