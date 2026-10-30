# -*- coding: utf-8 -*-
"""[CLIENT_EMAIL_V1] お客様メールを同一現場の同期対象に追加する。"""
import io

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(P, encoding="utf-8").read()

old = "    k === 'payment_status' || k === 'payment_memo')"
new = ("    k === 'payment_status' || k === 'payment_memo' ||\n"
       "    // [CLIENT_EMAIL_V1] お客様メールは同じ現場なら同一のはずなので同期する\n"
       "    k === 'client_email')")
assert s.count(old) == 1, "anchor: %d" % s.count(old)
io.open(P, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("sibling sync updated")
