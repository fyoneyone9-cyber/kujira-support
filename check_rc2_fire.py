import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# RAPE_COMP_V2_R の挿入位置と、その後のwf['6']書き込みを確認
rc2_line = None
fp_overwrite_lines = []
for i, l in enumerate(lines):
    if 'RAPE_COMP_V2_RELOCATED' in l:
        rc2_line = i + 1
    if 'RAPE_COMP_V2_R' in l and 'print' in l:
        print(f'RC2Rログ行: L{i+1}')
    if rc2_line and i > rc2_line:
        if 'wf["6"]["inputs"]["text"]' in l or "wf['6']['inputs']['text']" in l:
            fp_overwrite_lines.append(i + 1)

print(f'RAPE_COMP_V2_R挿入: L{rc2_line}')
print(f'その後のwf[6]書き込み件数: {len(fp_overwrite_lines)}')
print(f'最初の5件: {fp_overwrite_lines[:5]}')
print(f'最後の5件: {fp_overwrite_lines[-5:]}')

# full_positive をwf['6']に書くのは何行目？
for i, l in enumerate(lines):
    if 'full_positive' in l and "wf[" in l and 'text' in l:
        print(f'L{i+1}: {l.rstrip()}')
