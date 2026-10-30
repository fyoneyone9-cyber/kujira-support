import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# jk_Aの完全定義を取得
idx = content.find("id: 'char_rohypnol_jk_A'")
if idx == -1:
    print("NOT FOUND")
else:
    # push({}); の終わりを探す
    start = content.rfind('window.CHAR_TEMPLATES', 0, idx)
    end = content.find(');', idx) + 2
    print(content[start:end][:2000])
