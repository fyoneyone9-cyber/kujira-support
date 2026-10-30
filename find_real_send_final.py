import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# REAL_USDU や waisnack_real経路の最終ポジ確認ログ直後のrequests.postを探す
for i, l in enumerate(lines):
    if 'REAL_USDU' in l or 'FINAL_NEG_LEN' in l or 'FINAL_POS_LEN' in l:
        print(f'L{i+1}: {l.rstrip()}')

print()
# 実際のPOST送信（_comfy_url へのPOST）
for i, l in enumerate(lines):
    if '_comfy_url' in l and 'post' in l.lower() and 'requests' in l:
        print(f'L{i+1}: {l.rstrip()[:100]}')
