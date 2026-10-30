# 入力: dashboard.html / 出力: defineSharedGenre等の呼び出し一覧（key, 位置, シーン数, シーズン構造）
import re, json
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8', errors='ignore').read()
calls = []
for m in re.finditer(r'(defineSharedGenre|defineGenrePack)\s*\(\s*\{', s):
    i = m.start()
    seg = s[i:i+600]
    k = re.search(r"key\s*:\s*['\"]([^'\"]+)", seg)
    calls.append((m.group(1), i, k.group(1) if k else '?'))
print(len(calls))
for c in calls:
    print(c)
