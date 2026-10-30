import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

for char_id, label in [('char_kakuseizai_s3_ff_tifa', 'S3_tifa'), ('char_kakuseizai_s3_ff_aerith', 'S3_aerith')]:
    idx = content.find(f"id:'{char_id}'")
    if idx < 0:
        print(f'{label}: NOT FOUND')
        continue
    # outfits を探す
    oi = content.find("outfits:", idx)
    start = content.find('[', oi)
    # JS形式のlabelを探す
    chunk = content[start:start+60000]
    labels = re.findall(r"'label':'([^']+)'", chunk)
    print(f'{label}: {len(labels)}シーン')
    for i, l in enumerate(labels):
        print(f'  {i:02d}: {l}')
    print()
