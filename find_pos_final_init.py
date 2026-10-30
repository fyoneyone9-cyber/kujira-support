import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# _pos_final の最初の代入（初期化）を探す
for i, l in enumerate(lines):
    if i < 40000: continue
    if i >= 43534: break
    # 右辺が_bypass_posや_wf6_textなどから始まる初期代入
    stripped = l.lstrip()
    if stripped.startswith('_pos_final') and '=' in stripped and '==' not in stripped:
        print(f'L{i+1}: {l.rstrip()[:200]}')
