import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)
print(f'バックアップ: {bak}')

# 現在のpromptを確認して置換
OLD_TIFA = "(young woman:1.6),(slender:1.6),(tifa lockhart:1.9),(final fantasy:1.8),(ff7:1.8), 20 years old, long black hair, white tank top torn, black miniskirt pushed aside, suspenders, large breasts"
NEW_TIFA  = "(tifa lockhart:1.9),(final fantasy:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(large breasts:1.5), 20 years old, long black hair"

OLD_AERITH = "(young woman:1.6),(slender:1.6),(aerith gainsborough:1.9),(final fantasy:1.8),(ff7:1.8), 22 years old, long brown hair in braid with pink ribbon disheveled, pink dress torn, medium breasts"
NEW_AERITH  = "(aerith gainsborough:1.9),(final fantasy:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(medium breasts:1.5), 22 years old, long brown braided hair, pink ribbon"

replacements = [
    (OLD_TIFA, NEW_TIFA, 'char_rape_ff_tifa'),
    (OLD_AERITH, NEW_AERITH, 'char_rape_ff_aerith'),
]

for old, new, cid in replacements:
    if old in content:
        content = content.replace(old, new, 1)
        print(f'{cid}: prompt修正OK')
    else:
        print(f'{cid}: WARNING - old prompt not found, checking...')
        idx = content.find(cid)
        if idx > 0:
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
print('完了')
