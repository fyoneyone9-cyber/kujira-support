import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/AI/ComfyUI/dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# S2のティファを参照用に取得
idx = content.find("char_kakuseizai_s2_tifa")
print("=== S2 tifa ブロック ===")
print(repr(content[idx-5:idx+600]))
