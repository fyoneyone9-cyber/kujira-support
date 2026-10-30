import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)

CHARS = {
    'char_rape_ff_tifa':   ('Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors', 0.65),
    'char_rape_ff_aerith': ('aerith_illu.safetensors', 0.65),
}

for char_id, (lora_name, lora_str) in CHARS.items():
    idx = content.find(f"'{char_id}'")
    push_start = content.rfind('window.CHAR_TEMPLATES.female.push({', 0, idx)
    push_end = content.find('});', idx) + 3
    block = content[push_start:push_end]

    # ブロック末尾のサンプル確認
    print(f'{char_id} 末尾200chars:')
    print(repr(block[-200:]))
    print()

    # outfits:[ ... ] の閉じ ] の直後（ブロック末尾 }); の直前）にloraを追加
    # 構造: ..., outfits:[...] });
    # ]; の後 }); の前に lora1/lora1_strength を追加
    # outfitsの閉じ ] を探す
    # ブロック内の最後の ] を探す
    last_bracket = block.rfind(']')
    if last_bracket < 0:
        print(f'{char_id}: ] not found')
        continue

    # ]の後から }); の前に挿入
    after_bracket = block[last_bracket+1:].strip()
    print(f'after_bracket: {repr(after_bracket)}')

    # ]の後に ,\n  lora1:..., lora1_strength:... を追加
    insert_str = f",\n    lora1:'{lora_name}',\n    lora1_strength:{lora_str}"
    new_block = block[:last_bracket+1] + insert_str + block[last_bracket+1:]

    content = content[:push_start] + new_block + content[push_end:]
    print(f'{char_id}: lora追加OK')

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
for char_id in CHARS:
    cidx = check.find(f"'{char_id}'")
    chunk = check[cidx:cidx+3000]
    lora_m = re.search(r"lora1:'([^']+)'", chunk)
    str_m = re.search(r"lora1_strength:([\d.]+)", chunk)
    print(f'  {char_id}: lora={lora_m.group(1) if lora_m else "NONE"} str={str_m.group(1) if str_m else "?"}')
print('完了')
