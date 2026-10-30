import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17]
inner = sc17.group(1)
lines = inner.split('\n')

# 65058行のoutfitsの完全な内容確認
line = lines[65057]  # 0-indexed
print('outfits line length:', len(line))
print('ends with:', repr(line[-50:]))

# この行全体のブレースバランスをチェック
depth = 0; in_str = False; sc_char = None
for c in line:
    if in_str:
        if c == '\\': continue
        if c == sc_char: in_str = False
    else:
        if c in ('"', "'"): in_str = True; sc_char = c
        elif c == '[' or c == '{': depth += 1
        elif c == ']' or c == '}': depth -= 1
print('Brace depth at end of outfits line:', depth, '(0=balanced, >0=unclosed)')

# 65060の }); 前の実際のHTMLコンテンツ
# このブロックのpush( がどこから始まるか
for j in range(65050, 0, -1):
    if 'push(' in lines[j]:
        print('push( found at block17 line', j+1, ':', repr(lines[j][:80]))
        break
