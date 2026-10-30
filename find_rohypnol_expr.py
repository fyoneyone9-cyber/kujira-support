import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# 1. rohypnol/drug_sleep/unconscious 関連の特別処理があるか
# 2. EXPR_FALLBACK の pain 判定条件
# 3. INSERTION_DEPTH_PHASE の発火条件（torn/ripped が引っかかるか）

targets = [
    'rohypnol',
    'drug_sleep',
    'ROHYPNOL',
    'drug induced sleep',
    'DRUG_FALLBACK',
    'pained expression',
    'EXPR_FALLBACK',
]

print("=== 関連行 ===")
for i, l in enumerate(lines, 1):
    ll = l.lower()
    for t in targets:
        if t.lower() in ll:
            print(i, repr(l.rstrip()[:130]))
            break
