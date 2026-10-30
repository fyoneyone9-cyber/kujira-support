import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# char_rape の最初のキャラを探す
for j, l in enumerate(lines):
    if 'char_rape_' in l:
        first_rape = j
        break
print(f"First rape char at line {first_rape+1}")
print(f"Lines {first_rape-15} to {first_rape+5}:")
for k in range(max(0,first_rape-15), first_rape+6):
    print(k+1, repr(lines[k][:100]))
