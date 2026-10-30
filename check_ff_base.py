import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

targets = ['char_rape_ff_tifa','char_rape_ff_aerith','char_rape30_ff_tifa','char_rape30_ff_aerith']
for tid in targets:
    idx = content.find("'" + tid + "'")
    if idx == -1:
        idx = content.find('"' + tid + '"')
    if idx == -1:
        print(tid, ': NOT FOUND'); continue
    chunk = content[idx:idx+500]
    # base_prompt探す
    m = re.search(r'base_prompt\s*:\s*["\']([^"\']{0,300})', chunk)
    if m:
        print(tid, '-> base:', m.group(1)[:200])
    else:
        print(tid, '-> chunk head:', chunk[:300])
    print()
