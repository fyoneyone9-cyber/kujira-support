import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
for cid in ['char_kakuseizai_peach', 'char_kakuseizai_mitsuri',
            'char_kakuseizai_s2_peach', 'char_kakuseizai_s2_mitsuri']:
    idx = content.find(f"id:'{cid}'")
    before = content[idx-50:idx]
    print(f"{cid}: {before!r}")
