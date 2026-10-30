import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# generateSinglePanel関数の定義を探して、その中のfetch/body部分を抜粋
in_func = False
depth = 0
start = 0
for i, l in enumerate(lines, 1):
    if 'function generateSinglePanel' in l or 'generateSinglePanel = ' in l or 'generateSinglePanel=async' in l:
        in_func = True
        start = i
        print(f'Function found at L{i}')
        break

if in_func:
    for i, l in enumerate(lines[start-1:start+200], start):
        if 'outfit' in l.lower() or 'panel' in l.lower() and ('char' in l.lower() or 'send' in l.lower()):
            print(i, repr(l.rstrip()[:160]))
