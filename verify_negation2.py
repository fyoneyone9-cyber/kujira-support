import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8') as f:
    content = f.read()

idx = content.find('obj.outfit_label_full')
if idx != -1:
    print("OK: negation code found in copy button")
    print(content[max(0,idx-50):idx+200])
else:
    print("NG")
