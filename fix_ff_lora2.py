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
    # push_end: }); を括弧の深さでカウント
    depth = 0
    i = push_start + len('window.CHAR_TEMPLATES.female.push(')
    push_end = -1
    while i < len(content):
        c = content[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                # }); を確認
                if content[i:i+3] in ('});', '}\n}', '} }'):
                    push_end = i + 3  # }); 含む
                else:
                    push_end = i + 1
                break
        i += 1

    if push_end < 0:
        print(f'{char_id}: push_end not found')
        continue

    block = content[push_start:push_end]
    print(f'{char_id}: block[{push_start}:{push_end}] len={len(block)}')
    print(f'  末尾: {repr(block[-80:])}')

    # すでにloraがあればスキップ
    if 'lora1:' in block:
        print(f'  lora1 already exists - skip')
        continue

    # }); の直前に挿入
    # block末尾は必ず \n}); か }); 
    if block.endswith('\n});'):
        new_block = block[:-4] + f",\n    lora1:'{lora_name}',\n    lora1_strength:{lora_str}\n}})"  + ';'
    elif block.endswith('});'):
        new_block = block[:-3] + f",lora1:'{lora_name}',lora1_strength:{lora_str}" + '});'
    else:
        print(f'  末尾形式不明: {repr(block[-20:])}')
        continue

    content = content[:push_start] + new_block + content[push_end:]
    print(f'  lora追加OK → 末尾: {repr(new_block[-80:])}')

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
    # ブロック末尾3000文字で確認
    chunk = check[cidx:cidx+100000]
    end = chunk.find('});')
    chunk2 = chunk[:end+3] if end > 0 else chunk[:3000]
    lora_m = re.search(r"lora1:'([^']+)'", chunk2)
    str_m = re.search(r"lora1_strength:([\d.]+)", chunk2)
    print(f'  {char_id}: lora={lora_m.group(1) if lora_m else "NONE"} str={str_m.group(1) if str_m else "?"}')
    print(f'  末尾: {repr(chunk2[-100:])}')
print('完了')
