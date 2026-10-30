import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
sc17_inner = scripts[17].group(1)
lines = sc17_inner.split('\n')

# 65060行の }); の前でpushを探す（広範囲）
for j in range(65059, 60000, -100):
    chunk = '\n'.join(lines[j-100:j])
    if 'CHAR_TEMPLATES.female.push(' in chunk:
        for k in range(j, j-100, -1):
            if 'CHAR_TEMPLATES.female.push(' in lines[k]:
                print(f"Found push at block17 line {k+1}:", repr(lines[k][:100]))
                # その push から 65060 の }) まで何行あるか
                print(f"  Gap: {65060 - (k+1)} lines")
                break
        break
else:
    print("No push found before line 65059")
