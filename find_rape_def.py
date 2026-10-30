import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# id:'char_rape_jk_A' の行を探す
for j, l in enumerate(lines):
    if "id: 'char_rape_jk_A'" in l or "id:'char_rape_jk_A'" in l:
        print(f"Found at line {j+1}")
        print(f"Lines {j-12} to {j+3}:")
        for k in range(max(0,j-12), j+4):
            print(k+1, repr(lines[k][:100]))
        break
