import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')

# 65060の }); が何に対応するか: 手前のpush(か [ を探す
depth_push = 0
for j in range(65059, max(0, 64900), -1):
    l = lines[j].strip()
    if l == '});': depth_push += 1
    elif 'CHAR_TEMPLATES' in l and 'push(' in l:
        depth_push -= 1
        if depth_push <= 0:
            print(f"Matching push at line {j+1}: {repr(lines[j][:80])}")
            break
    elif l.startswith('{') and not 'push' in l:
        print(f"Bare {{ at line {j+1}: {repr(lines[j][:60])}")

# 65040-65060周辺を広く表示
print("\nLines 65035-65062:")
for j in range(65034, 65063):
    if j < len(lines): print(j+1, repr(lines[j][:80]))
