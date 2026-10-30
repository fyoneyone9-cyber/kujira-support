import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard_backup_20261020_074027.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc17 = scripts[17]
lines = sc17.split('\n')
# push([ を探す
for j in range(len(lines)-1, -1, -1):
    l = lines[j].strip()
    if 'push([' in l or ('push(' in l and l.endswith('[')):
        print(f"Found push([ at line {j+1}: {repr(lines[j][:100])}")
        # このpushに対応するchar_rapeかkirokuが近くにあるか
        # 前後20行
        for k in range(max(0,j-2), min(len(lines), j+5)):
            print(k+1, repr(lines[k][:100]))
        break
