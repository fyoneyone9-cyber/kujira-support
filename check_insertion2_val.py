import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find('char_rohypnol_aerith')
chunk = content[idx:idx+120000]

# ラベルとvalueを同時に抽出
# まず「挿入②」の位置を直接探す
i2 = chunk.find('挿入②')
print(f'挿入② at offset={i2}')
print(chunk[max(0,i2-200):i2+400])
