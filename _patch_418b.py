# -*- coding: utf-8 -*-
"""[HYDRATION_FIX_V2] 残N日/N日超過の表示を mounted 後に限定する。

SSRはUTC、ブラウザはJSTで `new Date().setHours(0,0,0,0)` が別の瞬間になり、
日数が1日ズレてテキスト不一致(#418)になっていた。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_418b_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# ---- (1) 入金期限の「残N日 / N日超過」 (L298-305) ----
OLD1 = """            {(() => {
              const pd = it.dashboard_todos?.['payment_due_date'] as string
              if (!pd || it.payment_received) return null
              const d = Math.ceil((new Date(pd).getTime() - new Date().setHours(0,0,0,0)) / 86400000)"""
assert s.count(OLD1) == 1, "anchor1: %d" % s.count(OLD1)
NEW1 = """            {(() => {
              const pd = it.dashboard_todos?.['payment_due_date'] as string
              if (!pd || it.payment_received) return null
              // [HYDRATION_FIX_V2 2026-10-29] SSR(UTC)とブラウザ(JST)で
              //   new Date().setHours(0,0,0,0) の瞬間が異なり日数が1日ズレる。
              //   テキスト不一致(React #418)になるのでマウント後にだけ描画する。
              if (!mountedGlobal()) return null
              const d = Math.ceil((new Date(pd).getTime() - new Date().setHours(0,0,0,0)) / 86400000)"""
s = s.replace(OLD1, NEW1, 1)

# ---- (2) days21 の「残N日」 (L1301,1303) ----
OLD2 = """                        {val === null && warn && <span className="text-xs text-orange-300 animate-pulse font-bold">⚠️ 残{days21}日  連携設定を急いでください</span>}"""
assert s.count(OLD2) == 1, "anchor2: %d" % s.count(OLD2)
NEW2 = """                        {/* [HYDRATION_FIX_V2] 日数はSSRとCSRでズレるのでマウント後のみ */}
                        {mounted && val === null && warn && <span className="text-xs text-orange-300 animate-pulse font-bold">⚠️ 残{days21}日  連携設定を急いでください</span>}"""
s = s.replace(OLD2, NEW2, 1)

OLD3 = """                        {val === null && days21 !== null && days21 > 30 && <span className="text-xs text-slate-500">残{days21}日（30日前からアラート）</span>}"""
assert s.count(OLD3) == 1, "anchor3: %d" % s.count(OLD3)
NEW3 = """                        {mounted && val === null && days21 !== null && days21 > 30 && <span className="text-xs text-slate-500">残{days21}日（30日前からアラート）</span>}"""
s = s.replace(OLD3, NEW3, 1)

# ---- (3) mountedGlobal ヘルパを定義（PaymentSection は別コンポーネントで mounted を見られない） ----
OLD4 = "type Equipment = { name?: string; value?: string }"
assert s.count(OLD4) == 1, "anchor4"
NEW4 = """// [HYDRATION_FIX_V2 2026-10-29] SSR中かどうかを返す。
//   日付差分など「サーバーとブラウザで必ず値が変わる表示」はマウント後に限定する。
//   React #418 (text content mismatch) の対策。
let __mounted = false
if (typeof window !== 'undefined') {
  // クライアントバンドルが評価された時点で true
  __mounted = true
}
function mountedGlobal() { return __mounted }

type Equipment = { name?: string; value?: string }"""
s = s.replace(OLD4, NEW4, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
