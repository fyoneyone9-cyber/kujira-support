"""S2のoutfits形式に対応してピーチ・蜜璃を再生成・再挿入"""
import sys, re, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

def extract_outfits_array(content, char_id_str):
    idx = content.find(char_id_str)
    if idx < 0: return None, -1, -1
    oi = content.find('outfits:[', idx)
    if oi < 0: return None, -1, -1
    start = content.find('[', oi)
    depth = 0; in_str = False; sc = None; i = start
    while i < len(content):
        c = content[i]
        if in_str:
            if c == '\\': i += 2; continue
            if c == sc: in_str = False
        else:
            if c in ('"', "'"): in_str = True; sc = c
            elif c == '[': depth += 1
            elif c == ']':
                depth -= 1
                if depth == 0: return content[start:i+1], start, i+1
        i += 1
    return None, -1, -1

def parse_unquoted_key_outfits(raw):
    """label:"...",value:"..." 形式を抽出"""
    return re.findall(r'\{label:"([^"]*)",value:"([^"]*)"\}', raw)

def make_js_outfits(pairs):
    items = []
    for label, value in pairs:
        le = label.replace("'", "\\'")
        ve = value.replace("'", "\\'")
        items.append(f"{{'label':'{le}','value':'{ve}'}}")
    return "[" + ",".join(items) + "]"

# S2 tifa のoutfits取得
s2_raw, _, _ = extract_outfits_array(content, "char_kakuseizai_s2_tifa'")
s2_outfits = parse_unquoted_key_outfits(s2_raw)
print(f"S2 tifa outfits: {len(s2_outfits)}")
if s2_outfits:
    print(f"  first: {s2_outfits[0][0]}")

S2_TIFA_CHAR = "Tifa Lockhart,Final Fantasy VII,long black hair dolphin-tail split,red eyes,athletic"
PEACH_CHAR   = "Princess Peach,Super Mario,blonde hair,blue eyes,medium breasts,slender body,pink princess dress,golden crown,white gloves"
MITSURI_CHAR = "Kanroji Mitsuri,Demon Slayer,long pink green gradient hair,green eyes,large breasts,voluptuous body,love pillar uniform,pink haori"
PEACH_NEG    = "(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls"
MITSURI_NEG  = "(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls"

def make_s2_outfits(outfits, new_char):
    pairs = []
    for label, value in outfits:
        nv = value.replace(S2_TIFA_CHAR, new_char)
        pairs.append((label, nv))
    return make_js_outfits(pairs)

peach_s2_js   = make_s2_outfits(s2_outfits, PEACH_CHAR)
mitsuri_s2_js = make_s2_outfits(s2_outfits, MITSURI_CHAR)

# 既存の間違ったS2ブロックを削除して正しいものに差し替え
def char_block(char_id, label, prompt, neg, outfits_js):
    p = prompt.replace("'", "\\'")
    n = neg.replace("'", "\\'")
    return f""",
{{
  id:'{char_id}',label:"{label}",gender:'female',
  prompt:'{p}',
  neg:'{n}',
  outfits:{outfits_js}
}}"""

# 既存の空outfitsのS2ブロックを削除
# char_kakuseizai_s2_peach と char_kakuseizai_s2_mitsuri のブロックを特定して削除
def remove_char_block(content, char_id):
    search = f"id:'{char_id}'"
    idx = content.find(search)
    if idx < 0:
        print(f"  {char_id}: not found, skip")
        return content
    # このブロックの開始(,\n{)を探す
    block_start = content.rfind(',\n{', 0, idx)
    if block_start < 0:
        block_start = content.rfind('\n{', 0, idx)
    # outfitsの終わりを見つけてそこから}を探す
    raw, _, oe = extract_outfits_array(content, f"{char_id}'")
    if oe < 0:
        print(f"  {char_id}: outfits not found")
        return content
    block_end = content.find('\n}', oe) + 2
    removed = content[block_start:block_end]
    print(f"  Removing {char_id}: {len(removed)} chars")
    return content[:block_start] + content[block_end:]

content = remove_char_block(content, 'char_kakuseizai_s2_peach')
content = remove_char_block(content, 'char_kakuseizai_s2_mitsuri')

# S2_aerithの後に正しいブロックを挿入
def find_char_block_end(content, char_id_str):
    raw, _, end = extract_outfits_array(content, char_id_str)
    if end < 0: return -1
    close = content.find('\n}', end)
    return close + 2

s2_insert = find_char_block_end(content, "char_kakuseizai_s2_aerith'")
print(f"S2 insert pos: {s2_insert}, context: {content[s2_insert-5:s2_insert+40]!r}")

blocks = (
    char_block('char_kakuseizai_s2_peach',   '💊覚醒剤S2 👸ピーチ姫',   PEACH_CHAR,   PEACH_NEG,   peach_s2_js) +
    char_block('char_kakuseizai_s2_mitsuri', '💊覚醒剤S2 🌸甘露寺蜜璃', MITSURI_CHAR, MITSURI_NEG, mitsuri_s2_js)
)

new_content = content[:s2_insert] + blocks + content[s2_insert:]

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', new_content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    new_content = new_content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"Version: {old_ver} -> {new_ver}")

backup = r'C:\AI\ComfyUI\dashboard_backup_s2fix_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html'
shutil.copy2(path, backup)
with open(path, 'w', encoding='utf-8') as f:
    f.write(new_content)
print("Saved.")

for cid in ['char_kakuseizai_s2_peach', 'char_kakuseizai_s2_mitsuri']:
    _, _, oe = extract_outfits_array(new_content, f"{cid}'")
    cnt = len(re.findall(r"'label':", new_content[new_content.find(f"id:'{cid}'"):oe]))
    print(f"  {cid}: outfits={cnt}")
