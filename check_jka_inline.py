import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# char_rape_jk_A を探す（全出現を確認）
hits = []
start = 0
while True:
    idx = content.find("char_rape_jk_A", start)
    if idx < 0: break
    hits.append(idx)
    start = idx + 1

print(f'char_rape_jk_A 出現: {len(hits)}箇所')
for h in hits[:5]:
    print(f'  pos={h}: {content[h-20:h+100]}')
    print()

# 最初のhitのキャラブロックを解析
idx = hits[0]
push_start = content.rfind('window.CHAR_TEMPLATES', 0, idx)
# このブロックのoutfitsを確認
chunk = content[push_start:push_start+500]
print('ブロック先頭:', chunk[:300])
