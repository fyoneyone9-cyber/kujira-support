import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'

with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# バックアップ
bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)
print(f'バックアップ: {bak}')

# donor = char_rape_jk_A のoutfitsブロックを取得
donor_id = 'char_rape_jk_A'
donor_pos = content.find(f"'{donor_id}'")
if donor_pos < 0:
    print('ERROR: donor not found')
    sys.exit(1)

# outfits: [ ... ] を抽出
chunk = content[donor_pos:donor_pos+500000]
ofs_m = re.search(r'outfits\s*:\s*\[', chunk)
if not ofs_m:
    print('ERROR: outfits not found')
    sys.exit(1)

bracket_start = donor_pos + ofs_m.start() + ofs_m.group().rfind('[')
depth = 0
i = bracket_start
while i < len(content):
    if content[i] == '[': depth += 1
    elif content[i] == ']':
        depth -= 1
        if depth == 0:
            bracket_end = i
            break
    i += 1

outfits_block = content[bracket_start:bracket_end+1]
print(f'outfitsブロック長: {len(outfits_block)} chars')

# 挿入するキャラ定義
CHARS = [
    {
        'id': 'char_rape_ff_tifa',
        'label': 'T ティファ・ロックハート（20歳）',
        'prompt': "(young woman:1.6),(slender:1.6),(tifa lockhart:1.9),(final fantasy:1.8),(ff7:1.8), 20 years old, long black hair, white tank top torn, black miniskirt pushed aside, suspenders, large breasts",
    },
    {
        'id': 'char_rape_ff_aerith',
        'label': 'U エアリス・ゲインズブール（22歳）',
        'prompt': "(young woman:1.6),(slender:1.6),(aerith gainsborough:1.9),(final fantasy:1.8),(ff7:1.8), 22 years old, long brown hair in braid with pink ribbon disheveled, pink dress torn, medium breasts",
    },
]

new_blocks = ''
for c in CHARS:
    new_blocks += f"""
window.CHAR_TEMPLATES.female.push({{
  id: '{c['id']}',
  label: '{c['label']}',
  gender: 'female',
  prompt: '{c['prompt']}',
  outfits: {outfits_block}
}});
"""

# 挿入位置: block22末尾の </script> 直前
# add_char.py と同じ基準点を使う
insert_marker = '/* [END_BLOCK22] */'
insert_pos = content.find(insert_marker)
if insert_pos < 0:
    # フォールバック: block22内の最後のpush().の後
    # "char_rohypnol_" 系の最後のpushを探す
    last_push = content.rfind("window.CHAR_TEMPLATES.female.push({", 0, len(content))
    # そのpushブロックの終端 });  を探す
    end_pos = content.find('});', last_push)
    insert_pos = end_pos + 3
    print(f'フォールバック挿入位置: {insert_pos}')
else:
    print(f'[END_BLOCK22] マーカー位置: {insert_pos}')

content = content[:insert_pos] + '\n' + new_blocks + content[insert_pos:]

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"')
    print(f'version: {old_ver} -> {new_ver}')

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)
print('書き込み完了')

# 検証
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    check = f.read()
for c in CHARS:
    found = f"'{c['id']}'" in check
    print(f"  {c['id']}: {'OK' if found else 'MISSING'}")
