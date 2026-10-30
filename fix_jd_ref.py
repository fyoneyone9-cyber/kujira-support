import sys, io, re, shutil
from datetime import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HTML = r'C:\AI\ComfyUI\dashboard.html'
with open(HTML, 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

bak = HTML.replace('.html', f'_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html')
shutil.copy2(HTML, bak)
print(f'バックアップ: {bak}')

# 修正対象: char_rape_jd_A/B/C, char_pov_rape_jd_A/B/C
# これらに outfits_ref:"S0091" を追加する
# 現在の末尾 patterns:[], }) の形を探して outfits_ref を挿入

fixed = 0
targets = [
    'char_rape_jd_A', 'char_rape_jd_B', 'char_rape_jd_C',
]

for cid in targets:
    # キャラブロックを探す
    idx = content.find(f"'{cid}'")
    if idx < 0:
        idx = content.find(f'"{cid}"')
    if idx < 0:
        print(f'{cid}: NOT FOUND')
        continue
    
    # そのブロックの終端 }); を探す
    chunk_start = idx
    end = content.find('});', chunk_start)
    if end < 0:
        print(f'{cid}: end not found')
        continue
    
    block = content[chunk_start:end+3]
    
    # すでにoutfits_refがあればスキップ
    if 'outfits_ref' in block or 'outfits:' in block:
        print(f'{cid}: already has outfits - skip')
        continue
    
    # patterns:[], の後に outfits_ref を追加
    # パターン: "patterns: []," の後
    old = '    patterns: [],\n\n  });'
    new = '    patterns: [],\n\n    outfits_ref:"S0091",\n\n  });'
    if old in block:
        new_block = block.replace(old, new, 1)
        content = content[:chunk_start] + new_block + content[chunk_start+len(block):]
        print(f'{cid}: outfits_ref:S0091 追加OK')
        fixed += 1
    else:
        # 別の終端形式を試す
        # '  });' の直前に追加
        alt_old = content[end-10:end+3]
        print(f'{cid}: patterns pattern not found, block末尾="{alt_old}"')
        print(f'  block: {block[-200:]}')

# POVレイプJDはインラインoutfitsが部分的にある → outfits_refを追加
print('\n=== char_pov_rape_jd 確認 ===')
for cid in ['char_pov_rape_jd_A', 'char_pov_rape_jd_B', 'char_pov_rape_jd_C']:
    idx = content.find(f"'{cid}'")
    if idx < 0:
        idx = content.find(f'"{cid}"')
    if idx < 0:
        print(f'{cid}: NOT FOUND')
        continue
    chunk = content[idx:idx+600]
    has_ref = 'outfits_ref' in chunk
    has_outfits = 'outfits:' in chunk
    outfit_count = len(re.findall(r'"label"', chunk))
    print(f'{cid}: ref={has_ref} outfits={has_outfits} count={outfit_count}')
    print(f'  {chunk[:400]}')
    print()

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"')
    print(f'version: {old_ver} -> {new_ver}')

with open(HTML, 'w', encoding='utf-8') as f:
    f.write(content)
print(f'\n修正完了: {fixed}体')
