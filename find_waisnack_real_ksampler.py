import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# waisnack_real経路でKSAMPLERをどう設定しているか
in_waisnack = False
for i, l in enumerate(lines):
    ll = l.lower()
    if 'waisnack_real' in ll or '_wai_real' in ll:
        if 'cfg' in ll or 'steps' in ll or 'sampler' in ll or 'ksampler' in ll:
            print(f"L{i+1}: {l.rstrip()[:160]}")
    # redcraft_solo_api.json 使用箇所
    if 'redcraft_solo_api' in ll:
        print(f"L{i+1}: {l.rstrip()[:160]}")
