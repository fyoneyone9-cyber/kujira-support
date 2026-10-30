import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find("'char_rape_jk_A'")
chunk = content[idx:idx+1000]
print('jk_A ブロック:')
print(chunk)
