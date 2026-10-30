import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard_backup_20261020_074027.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
# kiroku_B の定義を探す
idx = content.find("char_kiroku_B")
if idx < 0: print("Not found"); sys.exit()
# 前後100文字
start = max(0, idx-500)
end = min(len(content), idx+200)
print(repr(content[start:end]))
