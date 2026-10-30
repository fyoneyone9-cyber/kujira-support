import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17 = scripts[17].group(1)
lines = sc17.split('\n')

# nyuuji_C を探す
for j, l in enumerate(lines):
    if 'char_nyuuji_C' in l or 'nyuuji_C' in l:
        print(f"Found nyuuji_C at line {j+1}")
        print("Lines", j-2, "to", j+10, ":")
        for k in range(max(0,j-2), min(len(lines), j+11)):
            print(k+1, repr(lines[k][:100]))
        break

# 65055-65065 の push 構造
print("\nBlock17 65050-65066:")
for j in range(65049, 65067):
    if j < len(lines): print(j+1, repr(lines[j][:100]))
