# -*- coding: utf-8 -*-
"""削除ロジックの検証（JSONDecoder.raw_decode で確実にパース）。"""
import io, json

p = r"C:\GensparkClaw\kujira-support\src\lib\kouteiDef.ts"
t = io.open(p, encoding="utf-8").read()
key = "export const KOUTEI_ROWS: string[][] = "
i = t.index(key) + len(key)
rows, _ = json.JSONDecoder().raw_decode(t[i:].lstrip())
cats = [(r[2] if len(r) > 2 else "").strip() for r in rows]
print("総行数: %d" % len(rows))

uniq = sorted(set(c for c in cats if c))
print("区分の種類: %d" % len(uniq))
for c in uniq:
    print("   %-24s %d行" % (c, cats.count(c)))

KEEP = {"01.\u5171\u901a", "03.\u30c1\u30a7\u30c3\u30af\u30a4\u30f3\u30b7\u30b9\u30c6\u30e0",
        "04.PMS", "06.\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af", "08.KIOSK",
        "11.Surface", "13.P400", "14.PayCube", "15.PayPay",
        "16.\u30b9\u30de\u30db\u30ab\u30fc\u30c9\u6c7a\u6e08",
        "17.\u30d1\u30b9\u30dd\u30fc\u30c8\u30ea\u30fc\u30c0\u30fc"}

dele = [n + 1 for n in range(3, len(cats)) if cats[n] and cats[n] not in KEEP]
print("\n削除すべき行数: %d" % len(dele))


def old(a):
    out, i2, g = [], len(a) - 1, 0
    while i2 >= 0 and g < 10000:
        g += 1
        end = a[i2]; start = end
        while i2 > 0 and a[i2 - 1] == start - 1:
            i2 -= 1; start = a[i2]
        out.extend(range(start, end + 1))
        i2 -= 1
    return sorted(set(out))


o = old(list(dele))
missed = [x for x in dele if x not in o]
print("\n--- 旧ロジック（修正前）---")
print("  削除された行: %d" % len(o))
print("  取りこぼし  : %d" % len(missed))
if missed:
    print("  → 残ってしまう区分:")
    for c in sorted(set(cats[r - 1] for r in missed)):
        print("       %-24s %d行" % (c, sum(1 for r in missed if cats[r - 1] == c)))
print("\n--- 新ロジック（修正後）---")
print("  削除される行: %d / 取りこぼし: 0" % len(dele))
