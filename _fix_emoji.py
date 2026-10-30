# -*- coding: utf-8 -*-
"""JSXテキスト内で \u{1F4DD} 形式は使えない（文字列リテラル外のため）。実体の絵文字に置換。"""
import io
p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(p, encoding="utf-8").read()
old = "\\u{1F4DD} \u5bfe\u5fdc\u5c65\u6b74:"
assert s.count(old) == 1, "anchor %d" % s.count(old)
s = s.replace(old, "\U0001F4DD \u5bfe\u5fdc\u5c65\u6b74:", 1)
io.open(p, "w", encoding="utf-8").write(s)
print("fixed")
