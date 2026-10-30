# 19ジャンル書き直し作業: defineSharedGenre/definePackGenre 呼び出し位置とkeyを列挙
import re, sys
sys.stdout.reconfigure(encoding='utf-8')
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
calls = [(m.start(), m.group(1)) for m in re.finditer(r'(?:window\.)?(defineSharedGenre|definePackGenre)\s*\(\s*\{', s)]
print('calls:', len(calls))
for pos, name in calls:
    ctx = s[pos:pos+600]
    key = re.search(r"key\s*:\s*['\"]([^'\"]+)['\"]", ctx)
    label = re.search(r"label\s*:\s*['\"]([^'\"]+)['\"]", ctx)
    nsc = ctx.count("v:")
    print(pos, name, key.group(1) if key else '?', label.group(1) if label else '?')
