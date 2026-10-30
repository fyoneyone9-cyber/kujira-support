import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# "let body = {" または "body = {" の定義を探す（985000〜1010000）
target = content[985000:1010000]
hits = [m.start() for m in re.finditer(r'(?:let|const|var)\s+body\s*=\s*\{|body\s*=\s*\{', target)]
print(f"body = {{ hits: {len(hits)}")
for pos in hits[:3]:
    print(f"\n--- abs={985000+pos} ---")
    print(target[pos:pos+1500])
    print("---")
