# -*- coding: utf-8 -*-
import io
P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
L = io.open(P, encoding="utf-8").read().split("\n")
hits = [i for i, l in enumerate(L) if "PAYPAY_APPLY" in l or "PayPay\u5229\u7528\u7533\u8acb" in l]
print("hits:", [h + 1 for h in hits])
if hits:
    a = hits[0] - 2
    for i in range(max(0, a), min(len(L), hits[0] + 14)):
        print("%5d| %s" % (i + 1, L[i][:120]))
