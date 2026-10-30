import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)

OLD_PROMPT = "(teenager:1.5),(petite:1.6),(slender:1.6),(sailor moon:1.9),(usagi tsukino:1.9), 16 years old, long blonde twin tails with odango buns disheveled, sailor moon costume torn and half removed, number collar 013 over white sailor collar, lying on back on institutional bed, day 009 of 30, eyes wet with tears streaming down, tiara removed lying beside her, photorealistic, high detail costume, 16 year old girl"

# キャラクター外見タグのみ（状況・状態・衣装状態タグを除去）
NEW_PROMPT = "(sailor moon:1.9),(usagi tsukino:1.9),(teenager:1.5),(petite:1.6),(slender:1.6),16 years old,long blonde twin tails,odango buns,blue eyes,fair skin"

if OLD_PROMPT in content:
    content = content.replace(OLD_PROMPT, NEW_PROMPT)
    print('char_rape30_sailor_moon prompt修正OK')
else:
    print('ERROR: old prompt not found')
    # 部分一致で確認
    idx = content.find('char_rape30_sailor_moon')
    print(content[idx:idx+400])

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"')
    print(f'version: {old_ver} -> {new_ver}')

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)

# 確認
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    check = f.read()
idx = check.find('char_rape30_sailor_moon')
print(check[idx:idx+300])
