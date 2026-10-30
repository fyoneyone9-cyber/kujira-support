import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# waisnack_real / redcraft ルートの送信点を特定
# "_payload = {"prompt": wf" の行を全列挙
for i, l in enumerate(lines):
    if '_payload = {"prompt": wf' in l or "_payload = {'prompt': wf" in l:
        # 前後のコンテキストラベル
        ctx = ''
        for j in range(max(0,i-20), i):
            if 'waisnack' in lines[j].lower() or 'redcraft' in lines[j].lower() or 'REAL' in lines[j] or 'real' in lines[j].lower():
                ctx = lines[j].strip()[:60]
                break
        print(f'L{i+1}: {l.rstrip()[:80]}  | ctx={ctx}')
