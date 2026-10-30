import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/AI/ComfyUI/dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S2ティファのoutfits全件取得
idx = content.find("char_kakuseizai_s2_tifa")
block_start = idx
# outfits配列の終わりを探す（次のid:まで）
next_id = content.find("{id:'char_", idx+10)
block = content[block_start:next_id]

# outfitのlabelだけ抽出
labels = re.findall(r'label:"([^"]+)"', block)
print(f'S2 tifaのoutfit数: {len(labels)}')
for i, l in enumerate(labels):
    print(f'{i:02d}: {l}')

# S3の既存キャラを確認
s3_chars = re.findall(r"id:'(char_kakuseizai_s3_[^']+)'", content)
print(f'\nS3既存キャラ: {len(s3_chars)}体')
for c in s3_chars:
    print(f'  {c}')
