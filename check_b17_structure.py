import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard_backup_20261020_074027.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc17 = scripts[17]
lines = sc17.split('\n')
# 最後の60行
print("Original block17 last 60 lines:")
for j in range(len(lines)-60, len(lines)):
    print(j+1, repr(lines[j][:100]))
