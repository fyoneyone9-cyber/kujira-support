import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard_backup_20261020_074027.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc17 = scripts[17]
lines = sc17.split('\n')

# rape_nyuuji_C の後 (65060行以降) の様子
print("Original 65058-65095:")
for j in range(65057, 65096):
    if j < len(lines): print(j+1, repr(lines[j][:100]))
