import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/AI/ComfyUI/dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S2 tifaのブロック取得
idx_s2t = content.find("id:'char_kakuseizai_s2_tifa'")
next_id_s2t = content.find("{id:'char_", idx_s2t + 10)
s2_tifa_block = content[idx_s2t:next_id_s2t]

# outfits:[...] を抽出（],patterns の前まで）
m = re.search(r'outfits:\[(.+)\],patterns:', s2_tifa_block, re.DOTALL)
if not m:
    print("ERROR: outfits not found")
    print(repr(s2_tifa_block[-100:]))
    sys.exit(1)
s2_outfits_raw = m.group(1)
print(f"S2 tifa outfits length: {len(s2_outfits_raw)}")

TIFA_PROMPT = "Tifa Lockhart,Final Fantasy VII,long black hair dolphin-tail split,red eyes,athletic,(anime style:1.4),20 years old,slender body"
AERITH_PROMPT = "Aerith Gainsborough,Final Fantasy VII,light brown hair ponytail pink ribbon,green eyes,(anime style:1.4),22 years old,slender body"

# エアリス用outfits: ティファプロンプトをエアリスに差し替え
aerith_outfits = s2_outfits_raw.replace(TIFA_PROMPT, AERITH_PROMPT)

# 挿入するキャラブロック
new_chars = (
    "{id:'char_kakuseizai_s3_ff_tifa',label:\"💊覚醒剤S3 👊ティファ\",gender:'female',"
    f"prompt:'{TIFA_PROMPT},(1girl:2.0),(solo:1.8),(only one girl:1.8)',"
    f"outfits:[{s2_outfits_raw}],patterns:[]}},"
    "\n"
    "{id:'char_kakuseizai_s3_ff_aerith',label:\"💊覚醒剤S3 🌿エアリス\",gender:'female',"
    f"prompt:'{AERITH_PROMPT},(1girl:2.0),(solo:1.8),(only one girl:1.8)',"
    f"outfits:[{aerith_outfits}],patterns:[]}},"
    "\n"
)

# 挿入位置: jk_Cブロックの直後
idx_jkc = content.find("id:'char_kakuseizai_s3_jk_C'")
next_block = content.find("{id:'char_", idx_jkc + 10)
if next_block < 0:
    print("ERROR: jk_C next block not found")
    sys.exit(1)

content_new = content[:next_block] + new_chars + content[next_block:]

# バージョン更新
ver_match = re.search(r'content="(\d+)"', content_new)
if ver_match:
    old_ver = ver_match.group(1)
    new_ver = str(int(old_ver) + 1)
    content_new = content_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"version: {old_ver} -> {new_ver}")

with open('C:/AI/ComfyUI/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content_new)

print("完了")
c_t = content_new.count("char_kakuseizai_s3_ff_tifa")
c_a = content_new.count("char_kakuseizai_s3_ff_aerith")
print(f"tifa={c_t}, aerith={c_a}")
