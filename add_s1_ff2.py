"""
覚醒剤S1 にティファ・エアリスを追加
S1の最後のキャラ（ahegao系）の後に追加
"""
import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# S1 jk_A の outfits取得
jka_idx = content.find("char_kakuseizai_jk_A'")
oi = content.find('outfits:[', jka_idx)
start = content.find('[', oi)
depth = 0
in_string = False
i = start
while i < len(content):
    c = content[i]
    if in_string:
        if c == '\\': i += 2; continue
        if c == string_char: in_string = False
    else:
        if c in ('"', "'"):
            in_string = True
            string_char = c
        elif c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0: end = i+1; break
    i += 1

s1_outfits_raw = content[start:end]
outfits = re.findall(r'\{"label":\s*"([^"]+)",\s*"value":\s*"([^"]+)"\}', s1_outfits_raw)
print(f"S1 jk_A outfits: {len(outfits)}")

S1_CHAR = "(teenage girl:1.8),(young:1.7),(slender:1.6),(small breasts:1.5),(jk:1.6),16 years old,158cm,black long straight hair,school uniform"
TIFA_CHAR = "(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(long black hair:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),(black mini dress:1.2),(leather suspenders:1.1)"
AERITH_CHAR = "(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail pink ribbon:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2)"

def make_outfits_js(outfits, old_char, new_char):
    items = []
    for label, value in outfits:
        nv = value.replace(old_char, new_char)
        le = label.replace("'", "\\'")
        ve = nv.replace("'", "\\'")
        items.append(f"{{'label':'{le}','value':'{ve}'}}")
    return "[" + ",".join(items) + "]"

tifa_outfits_js = make_outfits_js(outfits, S1_CHAR, TIFA_CHAR)
aerith_outfits_js = make_outfits_js(outfits, S1_CHAR, AERITH_CHAR)

# S1の最後のキャラブロックを見つける
# S1のキャラは window.CHAR_TEMPLATES.female.push() 形式（S2以降と同じ）または直接配列定義
# youchien_Cが最後のS1キャラ。そのブロック終端を探す。
yc_idx = content.rfind("char_kakuseizai_youchien_C'")

# このキャラブロックの } を探す（次のキャラブロックの前の },）
# S1ブロックは },\n{ 区切り
search_from = yc_idx
# outfits:[ の終端 + } を探す
oi = content.find('outfits:[', search_from)
oc_start = content.find('[', oi)
depth = 0
in_string = False
string_char = None
i = oc_start
while i < len(content):
    c = content[i]
    if in_string:
        if c == '\\': i += 2; continue
        if c == string_char: in_string = False
    else:
        if c in ('"', "'"): in_string = True; string_char = c
        elif c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0: outfits_end = i+1; break
    i += 1

# outfits_end の後の } を探す（キャラブロックの閉じ）
block_close = content.find('\n}', outfits_end)
# 次の { まで
insert_pos = block_close + 2  # \n} の後

# 実際の挿入位置を確認
print(f"Insert after: {content[outfits_end:outfits_end+50]!r}")
print(f"Insert pos context: {content[insert_pos-5:insert_pos+100]!r}")

# 新キャラブロックを作成
def make_char_block(char_id, label, prompt, neg, outfits_js):
    return f""",
{{
  id:'{char_id}',label:"{label}",gender:'female',
  prompt:'{prompt}',
  neg:'{neg}',
  outfits:{outfits_js}
}}"""

TIFA_NEG = "(adult:1.3),(mature:1.4),(middle aged:1.5),watermark,signature,text,logo,multiple girls"
AERITH_NEG = "(adult:1.3),(mature:1.4),(middle aged:1.5),watermark,signature,text,logo,multiple girls"

tifa_block = make_char_block(
    'char_kakuseizai_tifa',
    '💊覚醒剤S1 👊ティファ',
    TIFA_CHAR.replace("'", "\\'"),
    TIFA_NEG,
    tifa_outfits_js
)
aerith_block = make_char_block(
    'char_kakuseizai_aerith',
    '💊覚醒剤S1 🌿エアリス',
    AERITH_CHAR.replace("'", "\\'"),
    AERITH_NEG,
    aerith_outfits_js
)

# 挿入
new_content = content[:insert_pos] + tifa_block + aerith_block + content[insert_pos:]

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', new_content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    new_content = new_content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

# バックアップ
backup = r'C:\AI\ComfyUI\dashboard_backup_s1ff_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
shutil.copy2(path, backup)
print(f"Backup: {backup}")

# 保存
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print(f"Saved. Tifa+Aerith added to S1 (29 scenes each)")

# 確認
content2 = new_content
for cid in ["char_kakuseizai_tifa'", "char_kakuseizai_aerith'"]:
    found = cid in content2
    print(f"  {cid}: {'OK' if found else 'MISSING'}")
