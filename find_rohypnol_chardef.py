import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# char_rohypnol_jk_A の定義行を探す
for i, l in enumerate(lines, 1):
    if 'char_rohypnol_jk_A' in l:
        # 前後5行を表示
        start = max(0, i-3)
        end = min(len(lines), i+5)
        for j in range(start, end):
            print(j+1, repr(lines[j].rstrip()[:200]))
        print('---')
        break
