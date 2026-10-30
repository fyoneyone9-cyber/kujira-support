import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# ComfyUIへのrequests.post送信 (wfをPOSTする箇所)
for i, l in enumerate(lines):
    if 'requests' in l and '.post(' in l and ('8188' in l or 'comfy' in l.lower()):
        print(f'L{i+1}: {l.rstrip()}')

# return jsonify / return で生成結果を返す箇所（最後の処理）
print('\n--- 最終return前後 ---')
for i, l in enumerate(lines):
    if 'return jsonify' in l and ('image_path' in l or '_image_path' in l):
        print(f'L{i+1}: {l.rstrip()}')
