import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)
print(f'バックアップ: {bak}')

# 現在のchar_rape_jd_A/B/Cブロックを削除して outfits_ref:"S0091" の正しい形式で再作成
# まず現在の3キャラ定義の範囲を特定
jda_idx = content.find("'char_rape_jd_A'")
if jda_idx < 0: jda_idx = content.find('"char_rape_jd_A"')

# push開始位置
push_start = content.rfind('window.CHAR_TEMPLATES.female.push({', 0, jda_idx)

# char_rape_jd_C の後の }); まで
jdc_idx = content.find("char_rape_jd_C", jda_idx)
push_end = content.find('});', jdc_idx) + 3
# 改行も含める
while push_end < len(content) and content[push_end] in '\n\r':
    push_end += 1

old_block = content[push_start:push_end]
print(f'削除範囲: {push_start}〜{push_end} ({len(old_block)}chars)')
print(f'先頭: {old_block[:100]}')
print(f'末尾: {old_block[-100:]}')

# 新しいブロック（JKと同じ形式）
CHARS_JD = [
    {
        'id': 'char_rape_jd_A',
        'label': '🔞レイプJD-A 黒髪ロング・春',
        'prompt': "black hair,center part,wavy long hair,silky hair,20 years old,163cm,japanese college student,casual outfit,tote bag,slender,(college student:1.9),(young adult:1.8),(black long hair:1.8)",
    },
    {
        'id': 'char_rape_jd_B',
        'label': '🔞レイプJD-B 茶髪ミディアム・夏',
        'prompt': "medium brown hair,natural wave,shoulder length,20 years old,160cm,japanese college student,casual summer outfit,slender,(college student:1.9),(young adult:1.8),(brown hair:1.8)",
    },
    {
        'id': 'char_rape_jd_C',
        'label': '🔞レイプJD-C 金髪ポニテ・秋',
        'prompt': "blonde ponytail,side swept bangs,20 years old,162cm,japanese college student,casual autumn outfit,slender,(college student:1.9),(young adult:1.8),(blonde hair:1.8)",
    },
]

new_blocks = ''
for c in CHARS_JD:
    new_blocks += f"""window.CHAR_TEMPLATES.female.push({{
    id: '{c["id"]}',
    label: '{c["label"]}',
    gender: 'female',
    prompt: '{c["prompt"]}',
    patterns: [],
    outfits_ref:"S0091",
  }});
"""

content = content[:push_start] + new_blocks + content[push_end:]

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"')
    print(f'version: {old_ver} -> {new_ver}')

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)

# 検証
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    check = f.read()
for c in CHARS_JD:
    cidx = check.find(f"'{c['id']}'")
    chunk = check[cidx:cidx+400] if cidx >= 0 else ''
    has_ref = 'outfits_ref:"S0091"' in chunk
    has_inline = 'outfits:[' in chunk or 'outfits: [' in chunk
    print(f"  {c['id']}: found={cidx>=0} ref={has_ref} inline={has_inline}")

print('完了')
