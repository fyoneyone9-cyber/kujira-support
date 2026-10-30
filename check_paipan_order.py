import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

targets = {
    'apply_quality_rules': [],
    'POST_QR_DEDUPE_V1': [],
    'PAIPAN_FINAL_V1': [],
    'KREA2_PROMPT_COMPRESS_V1': [],
    '_age_hoist_global': [],
    '_solo_guard': [],
    'PAIPAN_INJECT_GLOBAL_V1': [],
    'weight_budget': [],
}

for i, l in enumerate(lines):
    for t in targets:
        if t in l:
            targets[t].append(i+1)

for t, lns in targets.items():
    print(f'{t}: lines {lns[:6]}')
