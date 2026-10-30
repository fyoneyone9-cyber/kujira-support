import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8') as f:
    content = f.read()

idx = content.find('outfit_label_full')
if idx != -1:
    print("OK: negation code found")
    print(content[idx:idx+300])
else:
    print("NG")
