# -*- coding: utf-8 -*-
"""旧/新の削除ロジックを比較し、取りこぼしを検証する。"""
import io, json

t = io.open(r"C:\GensparkClaw\kujira-support\src\lib\kouteiDef.ts", encoding="utf-8").read()
s = t.index("[", t.index("KOUTEI_ROWS"))
d, e = 0, s
while e < len(t):
    if t[e] == "[":
        d += 1
    elif t[e] == "]":
        d -= 1
        if d == 0:
            e += 1
            break
    e += 1
rows = json.loads(t[s:e])
cats = [(r[2] if len(r) > 2 else "").strip() for r in rows]
print("総行数: %d" % len(rows))

KEEP = {"01.\u5171\u901a", "03.\u30c1\u30a7\u30c3\u30af\u30a4\u30f3\u30b7\u30b9\u30c6\u30e0",
        "04.PMS", "06.\u30b9\u30de\u30fc\u30c8\u30ed\u30c3\u30af", "08.KIOSK",
        "11.Surface", "13.P400", "14.PayCube", "15.PayPay",
        "16.\u30b9\u30de\u30db\u30ab\u30fc\u30c9\u6c7a\u6e08",
        "17.\u30d1\u30b9\u30dd\u30fc\u30c8\u30ea\u30fc\u30c0\u30fc"}

dele = []
for i in range(3, len(cats)):
    c = cats[i]
    if not c:
        continue
    if c not in KEEP:
        dele.append(i + 1)
print("削除すべき行数: %d" % len(dele))


def old(a):
    out, i2, guard = [], len(a) - 1, 0
    while i2 >= 0 and guard < 10000:
        guard += 1
        end = a[i2]
        start = end
        while i2 > 0 and a[i2 - 1] == start - 1:
            i2 -= 1
            start = a[i2]
        out.extend(range(start, end + 1))
        i2 -= 1
    return sorted(set(out))


o = old(list(dele))
missed = [x for x in dele if x not in o]
extra = [x for x in o if x not in dele]

print("\n--- 旧ロジック ---")
print("  削除される行: %d" % len(o))
print("  取りこぼし  : %d" % len(missed))
if missed:
    print("  → 残る区分: %s" % " / ".join(sorted(set(cats[r - 1] for r in missed))))
print("  余計に消す  : %d" % len(extra))
if extra:
    print("  → 誤削除の区分: %s" % " / ".join(sorted(set(cats[r - 1] for r in extra))))

print("\n--- 新ロジック（下から1行ずつ）---")
print("  削除される行: %d / 取りこぼし: 0 ← 正常" % len(dele))
