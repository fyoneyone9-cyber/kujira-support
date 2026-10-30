"""
char_rape_ff_tifa / char_rape_ff_aerith:
1. outfitプロンプトからJK固有タグを除去
2. LoRAを設定（tifa/aerith）
"""
import sys, io, re, shutil, json
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)
print(f'バックアップ: {bak}')

# JK固有タグ（outfitプロンプトから除去する語）
JK_TAGS_RE = re.compile(
    r',?\s*(?:teenage girl|brown ponytail|school uniform|17 years old|'
    r'high school (?:girl|student|uniform)|white blouse|dark blazer|plaid pleated skirt|'
    r'knee-high socks|school bag|neat school uniform|'
    r'16 years? old|jk|japanese high school)',
    re.IGNORECASE
)

# ティファ用追加タグ
TIFA_ADD = "long black hair,20 years old,tifa lockhart,final fantasy,"
# エアリス用追加タグ  
AERITH_ADD = "long brown braided hair,22 years old,aerith gainsborough,final fantasy,"

fixed_tifa = 0
fixed_aerith = 0

def clean_outfit_value(val, char_add):
    """outfitのvalueからJKタグを除去してFFタグを追加"""
    cleaned = JK_TAGS_RE.sub('', val)
    # 先頭のカンマや余分なスペースを除去
    cleaned = re.sub(r'^[\s,]+', '', cleaned)
    cleaned = re.sub(r',\s*,', ',', cleaned)
    # まだFFタグがなければ追加
    if 'long black hair' not in cleaned and 'long brown' not in cleaned:
        cleaned = char_add + cleaned
    return cleaned

# char_rape_ff_tifa のブロックを探す
for char_id, char_add, lora_name, lora_strength in [
    ('char_rape_ff_tifa', TIFA_ADD, 'Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors', 0.65),
    ('char_rape_ff_aerith', AERITH_ADD, 'aerith_illu.safetensors', 0.65),
]:
    idx = content.find(f"'{char_id}'")
    if idx < 0: idx = content.find(f'"{char_id}"')
    if idx < 0:
        print(f'{char_id}: NOT FOUND')
        continue

    # push開始
    push_start = content.rfind('window.CHAR_TEMPLATES.female.push({', 0, idx)
    # push終端（});）
    push_end = content.find('});', idx) + 3
    block = content[push_start:push_end]

    # outfits の value フィールドを全て修正
    def replace_value(m):
        label = m.group(1)
        val = m.group(2)
        new_val = clean_outfit_value(val, char_add)
        return f'{{label:"{label}",value:"{new_val}"'

    new_block = re.sub(
        r'\{label:"([^"]+)",value:"([^"]+)"',
        replace_value,
        block
    )

    # LoRAを設定（lora1フィールドがあれば更新、なければ promptの後に追加）
    # lora1 フィールドを探して更新
    if 'lora1:' in new_block:
        new_block = re.sub(r"lora1:\s*['\"][^'\"]*['\"]", f"lora1:'{lora_name}'", new_block)
        new_block = re.sub(r"lora1_strength:\s*[\d.]+", f"lora1_strength:{lora_strength}", new_block)
        print(f'{char_id}: lora1 更新')
    else:
        # patterns:[], の前に追加
        new_block = new_block.replace(
            "    patterns: [],",
            f"    lora1:'{lora_name}',\n    lora1_strength:{lora_strength},\n    patterns: [],"
        )
        print(f'{char_id}: lora1 追加')

    content = content[:push_start] + new_block + content[push_end:]
    
    # 修正数カウント
    changed = len(re.findall(r'long black hair|long brown', new_block))
    if char_id == 'char_rape_ff_tifa':
        fixed_tifa = changed
    else:
        fixed_aerith = changed

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

for char_id in ['char_rape_ff_tifa', 'char_rape_ff_aerith']:
    cidx = check.find(f"'{char_id}'")
    chunk = check[cidx:cidx+1000] if cidx >= 0 else ''
    has_lora = 'lora1:' in chunk
    has_jk = 'teenage girl' in chunk or 'brown ponytail' in chunk or 'school uniform' in chunk
    has_ff = 'long black hair' in chunk or 'long brown' in chunk
    lora_name_found = re.search(r"lora1:'([^']+)'", chunk)
    print(f'  {char_id}: lora={has_lora}({lora_name_found.group(1) if lora_name_found else "?"}) jk_残={has_jk} ff_タグ={has_ff}')

print(f'\n完了 tifa:{fixed_tifa} aerith:{fixed_aerith}')
