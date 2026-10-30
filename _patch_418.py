# -*- coding: utf-8 -*-
"""[HYDRATION_FIX_V2 2026-10-29] React #418 を完全に潰す。

原因: 「残N日」「N日超過」をSSR時とブラウザ時で別々に計算していた。
  L301  const d = Math.ceil((new Date(pd).getTime() - new Date().setHours(0,0,0,0)) / 86400000)
  L302-303  <span>{-d}日超過!</span> / <span>残{d}日</span>
  L1248 const days21 = ... new Date().setHours(0,0,0,0) ...
  L1301,1303 <span>残{days21}日 …</span>

  サーバーはUTC基準、ブラウザはJST基準で `new Date().setHours(0,0,0,0)` が
  別の瞬間になるため日数が1日ズレ、テキスト不一致 = #418。

対策: これらの表示を mounted 後にだけ描画する。
  ・DueBadge(L301付近) は小コンポーネントなので useMounted を内部に持たせる
  ・IntegRow の days21 表示は親の mounted を参照する
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_418_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
L = io.open(P, encoding="utf-8").read().split("\n")

print("--- L296-308 ---")
for i in range(296, 309):
    print("%5d| %s" % (i, L[i - 1].rstrip()[:150]))
print("\n--- L1244-1252 ---")
for i in range(1244, 1253):
    print("%5d| %s" % (i, L[i - 1].rstrip()[:150]))
