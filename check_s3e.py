import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('C:/AI/ComfyUI/dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find("id:'char_kakuseizai_s2_tifa'")
next_id = content.find("{id:'char_", idx + 10)
block = content[idx:next_id]
print(f"block length: {len(block)}")
print("--- 末尾200文字 ---")
print(repr(block[-200:]))
