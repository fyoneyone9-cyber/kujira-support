import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# L32825〜L38593の間でindent=8のif/elif/else文を探す
# これらがkrea2のルート分岐かもしれない
for i, l in enumerate(lines):
    if i < 32824: continue
    if i >= 38592: break
    stripped = l.lstrip()
    indent = len(l) - len(stripped)
    if indent == 8 and (stripped.startswith('if ') or stripped.startswith('elif ') or stripped.startswith('else:') or stripped.startswith('try:') or stripped.startswith('except') or stripped.startswith('#')):
        print(f'L{i+1}: {l.rstrip()[:150]}')
