# -*- coding: utf-8 -*-
# 対象9グループのID実体数を正確に数える（苗床S等の巻き込み確認）
import re, sys, io, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8').read()

def ids(pat):
    return sorted(set(re.findall(r"id:\s*['\"](" + pat + r"[a-zA-Z0-9_]*)['\"]", s)))

groups = {
    'magic_youjo (✨魔法少女12)': r'char_magic_youjo_',
    'mahou_shoujo (✨魔法少女12)': r'char_mahou_shoujo_',
    'mahou全学年13': r'char_mahou_(?:youjo|shougaku|chuugaku|jk)_',
    'manga_mahou (漫画要21)': r'char_manga_mahou_',
    'tentacle46': r'char_tentacle_',
    'tentacle_elf6': r'char_tentacle_elf_',
    'tentacle_mahou6': r'char_tentacle_mahou_',
    'mahou_youchien5': r'char_mahou_youchien_',
}
for g, p in groups.items():
    r = ids(p)
    print(g, len(r))
    for x in r[:50]:
        print('   ', x)
