import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
idx = content.find('char_kiroku_A')
print('kiroku_A pos:', idx)
line_num = content[:idx].count('\n') + 1
print('Line:', line_num)
# 前後表示
before = content[idx-400:idx]
after = content[idx:idx+200]
print('Before:')
for i, l in enumerate(before.split('\n')[-8:]):
    print(' ', repr(l[:120]))
print('After:')
for i, l in enumerate(after.split('\n')[:5]):
    print(' ', repr(l[:120]))
