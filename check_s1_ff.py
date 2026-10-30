import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

checks = [
    ("char_kakuseizai_tifa", "S1 tifa"),
    ("char_kakuseizai_aerith", "S1 aerith"),
    ("char_kakuseizai_s2_tifa", "S2 tifa"),
    ("char_kakuseizai_s2_aerith", "S2 aerith"),
    ("char_kakuseizai_s3_ff_tifa", "S3 ff_tifa"),
    ("char_kakuseizai_s3_ff_aerith", "S3 ff_aerith"),
]
for cid, label in checks:
    found = cid + "'" in content or cid + '"' in content
    print(f"{label}: {'EXISTS' if found else 'MISSING'}")

# S2のtifa/aerithのoutfits数も確認
for cid in ["char_kakuseizai_s2_tifa", "char_kakuseizai_s2_aerith"]:
    idx = content.find(cid)
    if idx < 0:
        continue
    oi = content.find("outfits:", idx)
    if oi < 0 or oi - idx > 3000:
        continue
    start = content.find('[', oi)
    chunk = content[start:start+60000]
    labels_json = re.findall(r'"label":\s*"([^"]+)"', chunk)
    labels_js = re.findall(r"'label':\s*'([^']+)'", chunk)
    labels = labels_json + labels_js
    print(f"  {cid}: {len(labels)} outfits")
