import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')

# 65058行のoutfitsのブレースバランス
l = lines[65057]
print(f"Line 65058 length: {len(l)}")
print(f"  End: {repr(l[-50:])}")
d = 0
for c in l:
    if c == '[': d += 1
    elif c == ']': d -= 1
print(f"  Bracket balance: {d}")

# 65059 (空行), 65060 (});)
print(f"Line 65059: {repr(lines[65058])}")
print(f"Line 65060: {repr(lines[65059])}")

# 65048付近のpush開始を探す
print("\nLooking for push before 65058:")
for j in range(65057, max(0, 65020), -1):
    l2 = lines[j].strip()
    if 'CHAR_TEMPLATES' in l2 and 'push(' in l2:
        print(f"  Found push at line {j+1}: {repr(lines[j][:80])}")
        break
    if l2.startswith('[') or (l2 == '['):
        print(f"  Found array start at line {j+1}: {repr(lines[j][:80])}")
        break
