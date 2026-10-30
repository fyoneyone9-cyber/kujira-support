import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# _rc3_pos / _rc3_lo の最初の定義前後を見る
for i, l in enumerate(lines):
    if '_rc3_pos' in l and 'wf[' in l:
        print(f'L{i+1}: {l}', end='')
        # 前後5行
        for j in range(max(0, i-10), min(len(lines), i+5)):
            print(f'  L{j+1}: {lines[j]}', end='')
        break

# outfit_prompt がwf['6']に入るのはどこ？
print('\n--- outfit → wf[6] の書き込み箇所 ---')
for i, l in enumerate(lines):
    if ('outfit' in l.lower() or 'outfit_prompt' in l) and "wf['6']" in l:
        print(f'L{i+1}: {l}', end='')
