import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
idx = content.find("'char_kaizou_med_asuka'")
if idx < 0:
    idx = content.find('"char_kaizou_med_asuka"')
if idx > 0:
    start = content.rfind('window.CHAR_TEMPLATES', 0, idx)
    # promptとnegだけ取得
    block = content[start:start+600]
    print(block[:600])
