import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/AI/ComfyUI/dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S2 tifaのoutfitsブロックを丸ごと取得
idx_s2t = content.find("id:'char_kakuseizai_s2_tifa'")
next_id_s2t = content.find("{id:'char_", idx_s2t + 10)
s2_tifa_block = content[idx_s2t:next_id_s2t]

# outfits:[...] の中身を抽出
outfits_match = re.search(r'outfits:\[(.+)\]$', s2_tifa_block, re.DOTALL)
if not outfits_match:
    print("ERROR: outfits not found in S2 tifa block")
    sys.exit(1)
s2_outfits_raw = outfits_match.group(1)

# S3用にoutfitを変換する関数
# S3はFFキャラのプロンプトを注入する必要があるのでvalueのプロンプトを書き換え
def make_s3_outfits(char_prompt_base, char_name_en, s2_outfits_raw):
    """S2のoutfitsをS3キャラ用に変換（FF7キャラプロンプトに差し替え）"""
    # 各outfitのvalueのプロンプト先頭にキャラプロンプトを挿入
    # S2のvalue内にはS2キャラのpromptが含まれているので、それをS3キャラのに差し替え
    result = s2_outfits_raw
    return result

# S3ティファ用outfits（S2と同じシーン、ラベルはS3表記に変更）
def make_outfits_for_char(char_label_prefix, char_prompt, s2_outfits_raw):
    # ラベルの先頭を変更（"💊覚醒剤S2 👊ティファ" → char_label_prefix）
    # label:"00..." はそのまま使う（シーン名は同じ）
    # value内のキャラプロンプトを差し替え
    outfits_str = s2_outfits_raw
    # S2 tifaのキャラプロンプト部分を差し替え
    old_char = "Tifa Lockhart,Final Fantasy VII,long black hair dolphin-tail split,red eyes,athletic,(anime style:1.4),20 years old,slender body"
    if char_prompt != old_char:
        outfits_str = outfits_str.replace(old_char, char_prompt)
    return outfits_str

# キャラ定義
TIFA_PROMPT = "Tifa Lockhart,Final Fantasy VII,long black hair dolphin-tail split,red eyes,athletic,(anime style:1.4),20 years old,slender body"
AERITH_PROMPT = "Aerith Gainsborough,Final Fantasy VII,light brown hair ponytail pink ribbon,green eyes,(anime style:1.4),22 years old,slender body"

# S3ティファ outfits（S2と同一シーン）
tifa_outfits = make_outfits_for_char("💊覚醒剤S3 👊ティファ", TIFA_PROMPT, s2_outfits_raw)
aerith_outfits_raw = s2_outfits_raw.replace(TIFA_PROMPT, AERITH_PROMPT)

# 挿入するキャラブロック
new_chars = f"""{{id:'char_kakuseizai_s3_ff_tifa',label:"💊覚醒剤S3 👊ティファ",gender:'female',prompt:'{TIFA_PROMPT},(1girl:2.0),(solo:1.8),(only one girl:1.8)',outfits:[{tifa_outfits}]}},
{{id:'char_kakuseizai_s3_ff_aerith',label:"💊覚醒剤S3 🌿エアリス",gender:'female',prompt:'{AERITH_PROMPT},(1girl:2.0),(solo:1.8),(only one girl:1.8)',outfits:[{aerith_outfits_raw}]}},"""

# 挿入位置: S3最後のキャラ（jk_C）の直後
insert_after = "char_kakuseizai_s3_jk_C'"
idx_jkc = content.find(insert_after)
if idx_jkc < 0:
    print("ERROR: jk_C not found")
    sys.exit(1)

# jk_Cブロック終端（次の {id: まで）
next_block = content.find("{id:'char_", idx_jkc + 10)
insert_pos = next_block  # jk_Cの直後に挿入

content_new = content[:insert_pos] + new_chars + "\n" + content[insert_pos:]

# バージョン更新
ver_match = re.search(r'content="(\d+)"', content_new)
if ver_match:
    old_ver = ver_match.group(1)
    new_ver = str(int(old_ver) + 1)
    content_new = content_new.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"version: {old_ver} -> {new_ver}")

with open('C:/AI/ComfyUI/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content_new)

print("完了: S3 ティファ・エアリス追加")

# 確認
count_tifa = content_new.count("char_kakuseizai_s3_ff_tifa")
count_aerith = content_new.count("char_kakuseizai_s3_ff_aerith")
print(f"tifa出現数: {count_tifa}, aerith出現数: {count_aerith}")
