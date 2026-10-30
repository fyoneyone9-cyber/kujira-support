import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard_backup_20261020_074027.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc17 = scripts[17]
lines = sc17.split('\n')

# char_rape_nyuuji_C を探す
for j, l in enumerate(lines):
    if "char_rape_nyuuji_C" in l:
        print(f"Found at block17 line {j+1}")
        print(f"Lines {j-3} to {j+15}:")
        for k in range(max(0,j-3), min(len(lines), j+16)):
            print(k+1, repr(lines[k][:100]))
        break
