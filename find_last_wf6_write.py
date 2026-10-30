import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# wf['6']['inputs']['text'] への書き込み行を全列挙し最後の方を確認
all_writes = []
for i, l in enumerate(lines):
    if ("wf['6']['inputs']['text']" in l or 'wf["6"]["inputs"]["text"]' in l) and '=' in l and 'get(' not in l:
        all_writes.append(i + 1)

print(f'総書き込み数: {len(all_writes)}')
print(f'最後20件:')
for ln in all_writes[-20:]:
    with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
        lines2 = f.readlines()
    print(f'  L{ln}: {lines2[ln-1].rstrip()}')

# ComfyUIへのPOST（実際の送信）はどこ？
print('\n--- ComfyUI POST送信箇所 ---')
for i, l in enumerate(lines):
    if 'prompt_server' in l or 'queue_prompt' in l or 'api/prompt' in l or '/prompt' in l and 'requests' in l:
        print(f'L{i+1}: {l.rstrip()}')
        if len([x for x in lines if '/prompt' in x]) > 100:
            break
