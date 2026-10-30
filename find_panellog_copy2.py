import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# Panel Log コピーボタンを探す
for kw in ['✅ コピー済', 'copyPanelLog', 'panel_log', 'panelLog', 'copy.*log', 'Panel Log']:
    idx = content.find(kw)
    if idx != -1:
        print(f'=== {kw!r} at {idx} ===')
        print(content[max(0,idx-200):idx+400])
        print()
        break
