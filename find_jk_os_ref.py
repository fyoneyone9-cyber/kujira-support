import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# char_rape_jk_ 周辺の os_ 参照を探す
idx = content.find("'char_rape_jk_A'")
chunk = content[max(0,idx-500):idx+2000]
print('jk_A周辺:')
print(chunk)
print()

# os_ キーを全域で探す
os_hits = re.findall(r'os_[a-f0-9]{12}', content)
from collections import Counter
c = Counter(os_hits)
print(f'\nos_ キー種類: {len(c)}')
for k, n in c.most_common(10):
    print(f'  {k}: {n}回')
