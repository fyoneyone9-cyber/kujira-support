import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17_inner = scripts[17].group(1)
lines17 = sc17_inner.split('\n')

# 65074行の }); は何に対応しているか。
# 65074行より前のブレース深度を計算
chunk = '\n'.join(lines17[:65073])  # 65073行まで
depth = 0; in_str = False; sc_char = None
i = 0
while i < len(chunk):
    c = chunk[i]
    if in_str:
        if c == '\\': i += 2; continue
        if c == sc_char: in_str = False
    else:
        if c in ('"', "'"): in_str = True; sc_char = c
        elif c == '(' or c == '[' or c == '{': depth += 1
        elif c == ')' or c == ']' or c == '}': depth -= 1
    i += 1
print(f"Depth before line 65074: {depth}")
print(f"  (expected: depth=2 for push({{ content }}) pattern)")

# 65072行のoutfitsがバランス取れているか
outfits_line = lines17[65071]
d2 = 0; in_s = False; sc2 = None
for c in outfits_line:
    if in_s:
        if c == '\\': continue
        if c == sc2: in_s = False
    else:
        if c in ('"', "'"): in_s = True; sc2 = c
        elif c in ('[', '{'): d2 += 1
        elif c in (']', '}'): d2 -= 1
print(f"outfits line depth delta: {d2}")
