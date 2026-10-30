import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# バックグラウンド辞書の適用コードを探す
for i, l in enumerate(lines, 1):
    if 'op_reinject' in l and ('background' in l.lower() or 'bg' in l.lower() or 'room' in l.lower() or '改造' in l):
        print(f'{i}: {l}', end='')
    if i > 200:
        break

# "改造" が char_prompt にあるかチェックするコードを探す
print('\n--- bg apply logic ---')
for i, l in enumerate(lines, 1):
    if ('改造' in l or 'modification' in l) and ('bg' in l or 'background' in l or 'room' in l):
        if 100 < i < 500:
            print(f'{i}: {l}', end='')
