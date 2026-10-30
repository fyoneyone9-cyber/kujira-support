import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

def get_outfit_labels(prefix):
    idx = content.find(prefix)
    if idx < 0:
        return []
    # outfits:[ を探す
    oi = content.find('outfits:[', idx)
    if oi < 0 or oi - idx > 3000:
        oi = content.find('outfits: [', idx)
    if oi < 0 or oi - idx > 3000:
        return []
    start = content.find('[', oi)
    depth = 0
    for i in range(start, min(start+400000, len(content))):
        if content[i] == '[': depth += 1
        elif content[i] == ']':
            depth -= 1
            if depth == 0:
                end = i+1
                break
    chunk = content[start:end]
    return re.findall(r'"label":\s*"([^"]+)"', chunk)

for prefix, label in [
    ("char_kakuseizai_jk_A'", 'S1_jk_A'),
    ("char_kakuseizai_s2_jk_A'", 'S2_jk_A'),
    ("char_kakuseizai_s3_jk_A'", 'S3_jk_A'),
    ("char_kakuseizai_s2_tifa'", 'S2_tifa'),
    ("char_kakuseizai_s3_ff_tifa'", 'S3_tifa'),
]:
    labels = get_outfit_labels(prefix)
    print(f'\n=== {label} ({len(labels)}シーン) ===')
    for i, l in enumerate(labels):
        print(f'  {i:02d}: {l}')
