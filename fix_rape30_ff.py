import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)

# rape30_ff系キャラの一覧と正しいbase prompt
CHARS_30FF = {
    'char_rape30_ff_tifa': {
        'lora': 'Tifa_Lockhart_Nomura_Tetsuya-style_Ver2.0_IS.safetensors',
        'lora_str': 0.65,
        'clean_prompt': "(tifa lockhart:1.9),(final fantasy:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(large breasts:1.5),20 years old,long black hair",
    },
    'char_rape30_ff_aerith': {
        'lora': 'aerith_illu.safetensors',
        'lora_str': 0.65,
        'clean_prompt': "(aerith gainsborough:1.9),(final fantasy:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(medium breasts:1.5),22 years old,long brown braided hair,pink ribbon",
    },
}

fixed = 0
for cid, info in CHARS_30FF.items():
    idx = content.find(f"'{cid}'")
    if idx < 0: idx = content.find(f'"{cid}"')
    if idx < 0:
        print(f'{cid}: NOT FOUND')
        continue

    push_start = content.rfind('window.CHAR_TEMPLATES.female.push({', 0, idx)
    # 括弧の深さでpush終端を探す
    depth = 0
    i = push_start + len('window.CHAR_TEMPLATES.female.push(')
    push_end = -1
    while i < len(content):
        c = content[i]
        if c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                push_end = i + 3
                break
        i += 1

    block = content[push_start:push_end]

    # 現在のpromptを抽出して汚染チェック
    prompt_m = re.search(r"prompt:\s*'([^']{0,600})'", block)
    if not prompt_m:
        prompt_m = re.search(r'prompt:\s*"([^"]{0,600})"', block)
    current_prompt = prompt_m.group(1) if prompt_m else ''
    print(f'{cid}:')
    print(f'  現在prompt: {current_prompt[:120]}')

    new_block = block

    # 1. promptを差し替え
    if current_prompt and current_prompt != info['clean_prompt']:
        new_block = new_block.replace(f"prompt: '{current_prompt}'", f"prompt: '{info['clean_prompt']}'")
        if new_block == block:  # ダブルクォートも試す
            new_block = new_block.replace(f'prompt: "{current_prompt}"', f"prompt: '{info['clean_prompt']}'")
        print(f'  prompt: 修正OK')
    else:
        print(f'  prompt: 変更不要')

    # 2. loraが未設定なら追加
    if 'lora1:' not in new_block:
        # outfits配列の閉じ]の後に追加
        last_bracket = new_block.rfind(']')
        if last_bracket > 0:
            insert = f",\n    lora1:'{info['lora']}',\n    lora1_strength:{info['lora_str']}"
            new_block = new_block[:last_bracket+1] + insert + new_block[last_bracket+1:]
            print(f'  lora1: 追加OK ({info["lora"]})')
    else:
        print(f'  lora1: 既存')

    content = content[:push_start] + new_block + content[push_end:]
    fixed += 1

# また同様に api_server 側でも char_rape30_ff_ を lora自動適用対象に追加する必要あり
# （dashboard側でlora1設定したので不要になるが念のため確認）

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
for cid in CHARS_30FF:
    cidx = check.find(f"'{cid}'")
    depth = 0
    i = check.rfind('window.CHAR_TEMPLATES.female.push({', 0, cidx) + len('window.CHAR_TEMPLATES.female.push(')
    pe = -1
    while i < len(check):
        if check[i] == '{': depth += 1
        elif check[i] == '}':
            depth -= 1
            if depth == 0: pe = i+3; break
        i += 1
    chunk = check[cidx:pe] if pe>0 else check[cidx:cidx+500]
    lora_m = re.search(r"lora1:'([^']+)'", chunk)
    prompt_m = re.search(r"prompt:\s*'([^']{0,80})'", chunk)
    print(f'  {cid}: lora={lora_m.group(1)[:40] if lora_m else "NONE"} prompt={prompt_m.group(1)[:60] if prompt_m else "?"}')

print(f'\n完了 {fixed}体')
