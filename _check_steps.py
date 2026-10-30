# -*- coding: utf-8 -*-
import io, re
s = io.open(r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx",
            encoding="utf-8").read()
key = "\u96db\u5f62\u306e\u30b3\u30d4\u30fc\u3092\u4f5c\u308b"   # 雛形のコピーを作る
i = s.index(key)
seg = s[i - 600:i + 7000]
nums = re.findall(r'text-\[10px\]">(\d)</span>', seg)
print("手順番号:", nums)
# 各ステップの先頭テキスト
for m in re.finditer(r'text-\[10px\]">(\d)</span>\s*\n\s*<span>([^<]{0,60})', seg):
    print("  %s: %s" % (m.group(1), m.group(2).strip()[:50]))
