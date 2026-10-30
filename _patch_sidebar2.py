# -*- coding: utf-8 -*-
"""[HYDRATION_FIX_V3] MiniCalendar の return 直前に未マウントガードを入れる（行指定）。"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\components\Sidebar.tsx"
bak = P + ".bak_sidebar2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
L = io.open(P, encoding="utf-8").read().split("\n")

# MiniCalendar 関数の範囲を特定
start = None
for i, l in enumerate(L):
    if l.startswith("function MiniCalendar()"):
        start = i
        break
assert start is not None, "MiniCalendar not found"

# その中の最初の "  return (" を探す
ret = None
for i in range(start, min(start + 90, len(L))):
    if L[i].rstrip() == "  return (":
        ret = i
        break
assert ret is not None, "return not found"
print("return at L%d" % (ret + 1))

guard = """  // [HYDRATION_FIX_V3 2026-10-29] マウント前はカレンダーを描画しない。
  //   SSRとCSRで new Date() が異なり「2026年 10月」が食い違って
  //   React #418 (text content mismatch) になっていた。
  if (viewYear === null || viewMonth === null) {
    return <div className="px-3 py-3 border-b border-slate-700" style={{ minHeight: 190 }} />
  }
"""
L.insert(ret, guard)
io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("guard inserted")

# 時計部分の確認
s = "\n".join(L)
for i, l in enumerate(s.split("\n"), 1):
    if "timeStr" in l or ("getHours" in l and "now" in l):
        print("clock L%d| %s" % (i, l.strip()[:130]))
