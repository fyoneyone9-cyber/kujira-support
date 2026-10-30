import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

DASHBOARD = r'C:\AI\ComfyUI\dashboard.html'

with open(DASHBOARD, encoding='utf-8', errors='replace') as f:
    content = f.read()

OLD_PROMPT = '"prompt": "Asuka Langley Soryu,Neon Genesis Evangelion,fiery red hair,twin braids,blue eyes,strong personality,plugsuit,14 years old,slender,anime style"'
NEW_PROMPT = '"prompt": "Asuka Langley Soryu,Neon Genesis Evangelion,fiery red orange hair,twin braids,blue eyes,14 year old girl,youthful face,teenage girl,hospital gown,slender figure,(young face:1.3),(teenage:1.3),(petite:1.2),real person photo"'

if OLD_PROMPT not in content:
    print("NOT FOUND - check prompt string")
    print(repr(content[content.find('char_kaizou_med_asuka'):content.find('char_kaizou_med_asuka')+300]))
else:
    shutil.copy2(DASHBOARD, DASHBOARD.replace('.html', f'_backup_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.html'))
    content = content.replace(OLD_PROMPT, NEW_PROMPT, 1)
    # バージョン更新
    ver_m = re.search(r'content="(\d{10,})"', content)
    if ver_m:
        old_ver = ver_m.group(1)
        content = content.replace(f'content="{old_ver}"', f'content="{int(old_ver)+1}"', 1)
        print(f'version: {old_ver} -> {int(old_ver)+1}')
    with open(DASHBOARD, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Done')
