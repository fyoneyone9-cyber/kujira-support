import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if i < 20000: continue  # ヘッダをスキップ
    if ('krea2' in l.lower() or 'is_krea' in l.lower()) and ('if ' in l or 'wf_type' in l or 'def ' in l):
        print(f'L{i+1}: {l.rstrip()[:150]}')
    if i > 60000: break
