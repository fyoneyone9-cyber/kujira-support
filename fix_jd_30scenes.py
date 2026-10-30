import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S0091 の実体（outfitsブロック）を取得
# char_rape_jk_A のインラインoutfitsを探す
idx = content.find("'char_rape_jk_A'")
if idx < 0: idx = content.find('"char_rape_jk_A"')
chunk = content[idx:idx+300000]

# outfits: [ ... ] を抽出
ofs_m = re.search(r'outfits\s*:\s*\[', chunk)
if not ofs_m:
    print('ERROR: outfits not found in jk_A')
    sys.exit(1)

bracket_start = idx + ofs_m.start() + ofs_m.group().rfind('[')
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

# 最初30シーン分だけ切り出す
# outfit オブジェクトを分割して30個取得
obj_pattern = re.compile(r'\{[^{}]{0,2000}\}', re.DOTALL)
outfit_objs = obj_pattern.findall(outfits_block)
print(f'jk_A 全outfits: {len(outfit_objs)}個')

# 最初30個
first30 = outfit_objs[:30]
print(f'使用: {len(first30)}個')
for i, o in enumerate(first30[:5]):
    lm = re.search(r'"label"\s*:\s*"([^"]+)"', o)
    print(f'  [{i}] {lm.group(1) if lm else "?"}')
print('  ...')
lm = re.search(r'"label"\s*:\s*"([^"]+)"', first30[-1])
print(f'  [29] {lm.group(1) if lm else "?"}')

# 30シーンブロックを再構成
outfits_30 = '[\n' + ',\n'.join(first30) + '\n]'

# バックアップ
bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)
print(f'\nバックアップ: {bak}')

# char_rape_jd_A/B/C を修正
# 現在の構造: 3キャラが1pushに混在 → 正しい3キャラ独立pushに分離
# まず現状のJD定義全体を確認
jd_targets = {
    'char_rape_jd_A': {
        'label': '🔞レイプJD-A 黒髪ロング・春',
        'prompt': "black hair,center part,wavy long hair,silky hair,20 years old,163cm,japanese college student,casual outfit,tote bag,slender",
    },
    'char_rape_jd_B': {
        'label': '🔞レイプJD-B 茶髪ミディアム・夏',
        'prompt': "medium brown hair,natural wave,shoulder length,20 years old,160cm,japanese college student,casual summer outfit,slender",
    },
    'char_rape_jd_C': {
        'label': '🔞レイプJD-C 金髪ポニテ・秋',
        'prompt': "blonde ponytail,side swept bangs,20 years old,162cm,japanese college student,casual autumn outfit,slender",
    },
}

# 既存のJD push()ブロックをまるごと置換する
# 現在の char_rape_jd_A ブロック開始〜終端(});)を探す
jda_idx = content.find("'char_rape_jd_A'")
if jda_idx < 0: jda_idx = content.find('"char_rape_jd_A"')

# pushの開始位置
push_start = content.rfind('window.CHAR_TEMPLATES.female.push({', 0, jda_idx)
# pushの終端 }); を探す（3キャラ分を含む）
# });が連続して出てくるので、3回分探す
end_pos = jda_idx
found_ends = 0
search_from = jda_idx
# JD_Cまで含む終端を探す → char_rape_jd_C の後の });
jdc_idx = content.find("'char_rape_jd_C'", jda_idx)
if jdc_idx < 0: jdc_idx = content.find('"char_rape_jd_C"', jda_idx)
push_end = content.find('});', jdc_idx) + 3
print(f'\npush_start={push_start} push_end={push_end}')
print(f'旧ブロック先頭: {content[push_start:push_start+80]}')
print(f'旧ブロック末尾: {content[push_end-50:push_end]}')

# 新しい3つの独立pushブロックを生成
new_blocks = ''
for cid, info in jd_targets.items():
    new_blocks += f"""window.CHAR_TEMPLATES.female.push({{
  id: '{cid}',
  label: '{info["label"]}',
  gender: 'female',
  prompt: '{info["prompt"]}',
  outfits: {outfits_30}
}});
"""

# 置換
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
for cid in jd_targets:
    found = f"'{cid}'" in check or f'"{cid}"' in check
    # シーン数確認
    cidx = check.find(f"'{cid}'")
    if cidx < 0: cidx = check.find(f'"{cid}"')
    chunk2 = check[cidx:cidx+60000] if cidx >= 0 else ''
    labels = re.findall(r'"label"\s*:\s*"([^"]+)"', chunk2)[:35]
    print(f'  {cid}: found={found} scenes={len(labels)}')
print('完了')
