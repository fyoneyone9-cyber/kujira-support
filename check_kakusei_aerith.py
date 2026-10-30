import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

targets = ['char_kakuseizai_s3_ff_aerith', 'char_kakuseizai_s3_ff_tifa',
           'char_kakuseizai_s2_ff_aerith', 'char_kakuseizai_s2_ff_tifa']
for tid in targets:
    idx = content.find("'" + tid + "'")
    if idx == -1: idx = content.find('"' + tid + '"')
    if idx == -1: print(tid, ': NOT FOUND'); continue
    chunk = content[idx:idx+600]
    m = re.search(r"prompt\s*:\s*'([^']{0,400})'", chunk)
    if not m: m = re.search(r'prompt\s*:\s*"([^"]{0,400})"', chunk)
    print(tid)
    print('  prompt:', m.group(1)[:300] if m else 'NOT FOUND')
    print()
