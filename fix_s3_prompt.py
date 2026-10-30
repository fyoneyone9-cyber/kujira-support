import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/AI/ComfyUI/dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S3 FF tifa/aerith の prompt フィールドを空にする
# outfit値にすでにキャラ記述が含まれているため二重になっている

TIFA_FULL = "Tifa Lockhart,Final Fantasy VII,long black hair dolphin-tail split,red eyes,athletic,(anime style:1.4),20 years old,slender body,(1girl:2.0),(solo:1.8),(only one girl:1.8)"
AERITH_FULL = "Aerith Gainsborough,Final Fantasy VII,light brown hair ponytail pink ribbon,green eyes,(anime style:1.4),22 years old,slender body,(1girl:2.0),(solo:1.8),(only one girl:1.8)"

# tifa: prompt='<TIFA_FULL>' → prompt=''
old_t = f"id:'char_kakuseizai_s3_ff_tifa',label:\"💊覚醒剤S3 👊ティファ\",gender:'female',prompt:'{TIFA_FULL}'"
new_t = "id:'char_kakuseizai_s3_ff_tifa',label:\"💊覚醒剤S3 👊ティファ\",gender:'female',prompt:''"
if old_t in content:
    content = content.replace(old_t, new_t)
    print("tifa prompt: OK -> cleared")
else:
    print("tifa prompt: NOT FOUND")
    # 実際のprompt部分を確認
    idx = content.find("char_kakuseizai_s3_ff_tifa")
    print(repr(content[idx:idx+200]))

# aerith: prompt='<AERITH_FULL>' → prompt=''
old_a = f"id:'char_kakuseizai_s3_ff_aerith',label:\"💊覚醒剤S3 🌿エアリス\",gender:'female',prompt:'{AERITH_FULL}'"
new_a = "id:'char_kakuseizai_s3_ff_aerith',label:\"💊覚醒剤S3 🌿エアリス\",gender:'female',prompt:''"
if old_a in content:
    content = content.replace(old_a, new_a)
    print("aerith prompt: OK -> cleared")
else:
    print("aerith prompt: NOT FOUND")
    idx = content.find("char_kakuseizai_s3_ff_aerith")
    print(repr(content[idx:idx+200]))

# バージョン更新
ver_match = re.search(r'content="(\d+)"', content)
if ver_match:
    old_ver = ver_match.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"version: {old_ver} -> {new_ver}")

with open('C:/AI/ComfyUI/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("完了")
