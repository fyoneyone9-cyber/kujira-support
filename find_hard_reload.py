import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines, 1):
    if 'Hard Reload' in l or 'hardReload' in l or 'hard_reload' in l:
        print(i, repr(l.rstrip()[:150]))
