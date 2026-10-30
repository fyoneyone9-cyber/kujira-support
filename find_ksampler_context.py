import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# L8606(indent=8)を囲むindent<8の条件文を探す
TARGET = 8605  # 0-based
for i in range(TARGET, max(0, TARGET-200), -1):
    l = lines[i]
    stripped = l.lstrip()
    indent = len(l) - len(stripped)
    if indent < 8 and (stripped.startswith('if ') or stripped.startswith('elif ') or stripped.startswith('for ') or stripped.startswith('def ') or stripped.startswith('while ')):
        print(f"L{i+1}[{indent}]: {l.rstrip()[:120]}")
        if indent <= 4:
            break
