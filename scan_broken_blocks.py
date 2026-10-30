import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
# },\n{\n  id:'char_kakuseizai_ パターンを全て検索
broken = [(m.start(), m.group()) for m in re.finditer(r'\},\n\{(\n  id:\'char_kakuseizai_)', content)]
print(f"Broken patterns: {len(broken)}")
for pos, txt in broken:
    print(f"  pos={pos}: {content[pos:pos+60]!r}")
