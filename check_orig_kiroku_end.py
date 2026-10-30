import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard_backup_20261020_074027.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc17 = scripts[17]
lines = sc17.split('\n')
# kiroku_E を探す
for j, l in enumerate(lines):
    if "char_kiroku_E" in l:
        print(f"kiroku_E at line {j+1}")
        print(f"Lines {j-2} to {j+25}:")
        for k in range(max(0,j-2), min(len(lines), j+26)):
            print(k+1, repr(lines[k][:100]))
        break
