import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17_inner = scripts[17].group(1)
lines = sc17_inner.split('\n')

# 65060行は });  → この前後で深さを確認
# 65000行から65070行まで表示（pushやpush([ の開始を探す）
print('Searching for push([')
for j in range(65060, 60000, -1):
    l = lines[j]
    if 'push([' in l or 'push( [' in l:
        print(f'  push([ at line {j+1}:', repr(l[:100]))
        break
    if 'push({' in l:
        print(f'  push({{ at line {j+1}:', repr(l[:100]))
        break

# 65044-65065
print('\nLines 65044-65065:')
for j in range(65043, 65066):
    print(j+1, repr(lines[j][:120]))
