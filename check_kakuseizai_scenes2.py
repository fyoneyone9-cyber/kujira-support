import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# まずIDの書き方を確認
for prefix in ['char_kakuseizai_jk_A', 'char_kakuseizai_s2_jk_A', 'char_kakuseizai_s3_ff_tifa']:
    idx = content.find(prefix)
    if idx < 0:
        print(f'{prefix}: NOT FOUND AT ALL')
        continue
    print(f'{prefix} found at {idx}: ...{content[idx-20:idx+80]}...')
    print()
