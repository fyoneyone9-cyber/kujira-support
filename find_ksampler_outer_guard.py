import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# L8606(KREA2_KSAMPLERコメント)のindentと、それを囲む直近のif文を確認
TARGET = 8605  # 0-based = L8606
print(f"L{TARGET+1} indent: {len(lines[TARGET]) - len(lines[TARGET].lstrip())}")

# 上に遡って同じかより低いindentのif/for文を探す
target_indent = len(lines[TARGET]) - len(lines[TARGET].lstrip())
print(f"\n前後50行のindent確認:")
for i in range(max(0, TARGET-30), min(len(lines), TARGET+5)):
    l = lines[i]
    stripped = l.lstrip()
    indent = len(l) - len(stripped)
    marker = " <<<<" if indent <= target_indent and ('if ' in stripped or 'for ' in stripped or 'def ' in stripped) else ""
    if marker or i >= TARGET - 5:
        print(f"L{i+1}[{indent}]: {l.rstrip()[:100]}{marker}")
