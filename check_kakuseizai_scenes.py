import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

for prefix, label in [
    ('char_kakuseizai_jk_A', 'S1_jk_A'),
    ('char_kakuseizai_s2_jk_A', 'S2_jk_A'),
    ('char_kakuseizai_s3_jk_A', 'S3_jk_A'),
    ('char_kakuseizai_s2_tifa', 'S2_tifa'),
    ('char_kakuseizai_s3_ff_tifa', 'S3_tifa'),
    ('char_kakuseizai_s2_aerith', 'S2_aerith'),
    ('char_kakuseizai_s3_ff_aerith', 'S3_aerith'),
]:
    idx = content.find(f"id: '{prefix}'")
    if idx < 0:
        idx = content.find(f'id: "{prefix}"')
    if idx < 0:
        print(f'{label}: NOT FOUND')
        continue
    chunk = content[idx:idx+8000]
    # label: '...' or label: "..."
    scenes = re.findall(r"label:\s*['\"]([^'\"]+)['\"]", chunk)
    # outfits の label を取得 (最初の30件)
    print(f'{label}: {len(scenes)} labels')
    for i, s in enumerate(scenes[:30]):
        print(f'  [{i}] {s}')
    print()
