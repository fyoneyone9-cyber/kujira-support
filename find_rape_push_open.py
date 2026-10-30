import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
sc17 = scripts[17]
lines = sc17.split('\n')

# 65060付近より前にある push( を逆順探索（配列プッシュの開始）
print("Searching backwards from 65060 for push(:")
for j in range(65059, max(0, 60000), -1):
    l = lines[j].strip()
    if 'push(' in l:
        print(f"  Found push at line {j+1}: {repr(lines[j][:120])}")
        if j < 65055:  # rape_nyuujiCより前なら表示して止める
            break
