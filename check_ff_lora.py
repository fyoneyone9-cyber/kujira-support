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
    # キャラ定義終端（次の push( or });）まで
    chunk = content[idx:idx+1200]
    loras = re.findall(r'lora\w*\s*:\s*["\']([^"\']+)["\']', chunk)
    print(tid, '-> loras:', loras if loras else 'NONE')
