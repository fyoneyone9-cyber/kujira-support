import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

for i, l in enumerate(lines, 1):
    if 'rohypnol' in l.lower():
        print(i, repr(l.rstrip()[:150]))
        if i > 20:  # 最初の20件だけ
            break
