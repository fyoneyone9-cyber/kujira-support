import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')
# char_rape_jk_A を探してその前のpushを見る
for j, l in enumerate(lines):
    if 'char_rape_jk_A' in l:
        print(f"rape_jk_A at line {j+1}")
        print("Lines", j-8, "to", j+2, ":")
        for k in range(max(0,j-8), min(len(lines), j+3)):
            print(k+1, repr(lines[k][:100]))
        break
