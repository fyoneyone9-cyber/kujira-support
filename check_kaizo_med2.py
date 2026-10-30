import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# kaizo_med を含む行を探す
lines = content.split('\n')
for j, l in enumerate(lines):
    if ('kaizo_med' in l or 'kaizou_med' in l) and 'id' in l:
        print(j+1, repr(l[:120]))
