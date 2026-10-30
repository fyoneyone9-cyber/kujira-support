import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

markers = {
    'apply_quality_rules': None,
    'POST_QR_DEDUPE_V1': None,
    'PAIPAN_FINAL_V1': None,
    'weight_budget': None,
    'KREA2_PROMPT_COMPRESS_V1': None,
    'RAPE_COMP_V3_FINAL': None,
    'PROMPT_ORDER_V1': None,
    'CLOTHED_BOTTOM_LOCK': None,
    '_payload_r = {"prompt"': None,
}
for i, l in enumerate(lines):
    for k in markers:
        if markers[k] is None and k in l:
            markers[k] = i + 1

for k, v in markers.items():
    print(f'L{str(v):6}: {k}')
