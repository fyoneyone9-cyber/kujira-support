import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
# L41698のインデント確認
target_line = lines[41697]  # 0-indexed
target_indent = len(target_line) - len(target_line.lstrip())
print(f"L41698 indent={target_indent}: {target_line.rstrip()[:100]}")

# 同じインデントか浅いインデントで直前のif/else/elifを探す
for i in range(41697, -1, -1):
    l = lines[i]
    indent = len(l) - len(l.lstrip())
    stripped = l.lstrip()
    if indent < target_indent and (stripped.startswith('if ') or stripped.startswith('elif ') or stripped.startswith('else:') or stripped.startswith('try:') or stripped.startswith('except') or stripped.startswith('def ')):
        print(f'L{i+1} indent={indent}: {l.rstrip()[:200]}')
        if indent <= 4:
            break
