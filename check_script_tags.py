import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts_iter = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))
print("Script blocks count:", len(scripts_iter))
# block16, 17, 18の開始行
for i in [15, 16, 17, 18, 19, 20, 21, 22, 23]:
    sc = scripts_iter[i]
    start_line = content[:sc.start()].count('\n') + 1
    end_line = content[:sc.end()].count('\n') + 1
    inner_lines = sc.group(1).count('\n') + 1
    print(f"Block {i}: HTML lines {start_line}-{end_line} ({inner_lines} inner lines)")
