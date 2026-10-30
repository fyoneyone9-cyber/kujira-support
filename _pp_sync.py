# -*- coding: utf-8 -*-
"""[PAYPAY_APPLY_LOG_V1] PayPay申請情報を同一現場で同期する。
同じホテルなら申請は1回なので、片方だけ記録されると混乱する。
"""
import io

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(P, encoding="utf-8").read()

old = ("    k === 'payment_status' || k === 'payment_memo' ||\n"
       "    // [CLIENT_EMAIL_V1] お客様メールは同じ現場なら同一のはずなので同期する\n"
       "    k === 'client_email')")
new = ("    k === 'payment_status' || k === 'payment_memo' ||\n"
       "    // [CLIENT_EMAIL_V1] お客様メールは同じ現場なら同一のはずなので同期する\n"
       "    k === 'client_email' ||\n"
       "    // [PAYPAY_APPLY_LOG_V1] PayPay申請は現場に1回なので同期する\n"
       "    k === 'paypay_applied_at' || k === 'paypay_mid' || k === 'paypay_apply_memo')")
assert s.count(old) == 1, "anchor: %d" % s.count(old)
io.open(P, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("SIBLING_SYNC に paypay_* を追加")
