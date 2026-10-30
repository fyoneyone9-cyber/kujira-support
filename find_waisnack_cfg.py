import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# KREA2_KSAMPLERブロックが実際に到達するか確認
# _is_qw21_ks のwaisnack_realルート内での判定を探す
# waisnack_real の cfg 設定箇所を全部探す
TARGET_RANGE_START = 36000  # waisnack_real付近
TARGET_RANGE_END = 60000

for i, l in enumerate(lines[TARGET_RANGE_START:TARGET_RANGE_END], start=TARGET_RANGE_START+1):
    ll = l.lower()
    if ('"cfg"' in l or "'cfg'" in l) and ('inputs' in l or 'nd[' in l or 'wf[' in l):
        print(f"L{i}: {l.rstrip()[:160]}")
