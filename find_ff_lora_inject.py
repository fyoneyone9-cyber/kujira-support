import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# LoRA関連の注入箇所を全部特定
keywords = ['aerith', 'tifa', 'ff_lora', 'ff7_lora', 'lora_ff', 'lora:aerith', 'lora:tifa',
            'lora:ff', 'aerith_illu', 'tifa_illu', 'ff_tifa', 'ff_aerith',
            '<lora:', 'lora_inject', 'lora_name', '_lora_str', 'char_lora']

found = {}
for i, line in enumerate(lines):
    ll = line.lower()
    for kw in keywords:
        if kw in ll:
            found[i+1] = line.rstrip()
            break

for lineno in sorted(found.keys()):
    print(f'L{lineno}: {found[lineno][:160]}')
