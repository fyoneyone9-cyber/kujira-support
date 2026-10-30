# -*- coding: utf-8 -*-
"""[HYDRATION_FIX_V3 2026-10-29] React #418 の真犯人 = Sidebar の時計とカレンダー。

SSRとCSRのDOM差分を実測して特定:
    SSRのみ: "17:41" / "2026" "年" "10月"(バラけた状態)
    CSRのみ: "17:43" / "2026年 10月"
  → 現在時刻を描画しており、サーバー描画時とブラウザ描画時で必ずズレる。
     サイドバーなので **全ページで #418 が出ていた**。

対策: mounted 後にだけ時刻依存の表示を描画する。
  ・MiniCalendar: 初期値を固定し、マウント後に今日の年月へ合わせる
  ・時計(L115付近): マウント前は空表示
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\components\Sidebar.tsx"
bak = P + ".bak_hydration_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# ---- (1) MiniCalendar の初期値 ----
OLD1 = """function MiniCalendar() {
  const today = new Date()
  const [viewYear, setViewYear] = useState(today.getFullYear())
  const [viewMonth, setViewMonth] = useState(today.getMonth())"""
assert s.count(OLD1) == 1, "anchor1: %d" % s.count(OLD1)
NEW1 = """function MiniCalendar() {
  // [HYDRATION_FIX_V3 2026-10-29] SSRとCSRで new Date() が異なり
  //   「2026年 10月」の描画が食い違って React #418 になっていた。
  //   初期値は描画しない(null)で、マウント後に今日の年月を入れる。
  const [viewYear, setViewYear] = useState<number | null>(null)
  const [viewMonth, setViewMonth] = useState<number | null>(null)
  useEffect(() => {
    const t = new Date()
    setViewYear(t.getFullYear())
    setViewMonth(t.getMonth())
  }, [])
  const today = new Date()"""
s = s.replace(OLD1, NEW1, 1)

# ---- (2) 未マウント時は何も描画しない ----
OLD2 = """  return (
    <div className="px-3 py-3 border-b border-slate-700">
      {/* ヘッダー（月移動） */}"""
assert s.count(OLD2) == 1, "anchor2: %d" % s.count(OLD2)
NEW2 = """  // [HYDRATION_FIX_V3] マウント前はカレンダーを描画しない(SSRと一致させる)
  if (viewYear === null || viewMonth === null) {
    return <div className="px-3 py-3 border-b border-slate-700" style={{ minHeight: 190 }} />
  }

  return (
    <div className="px-3 py-3 border-b border-slate-700">
      {/* ヘッダー（月移動） */}"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched calendar")

# ---- (3) 時計部分を確認 ----
L = s.split("\n")
for i in range(105, 135):
    if i <= len(L):
        t = L[i - 1]
        if "getHours" in t or "timeStr" in t or "setInterval" in t:
            print("clock L%d| %s" % (i, t.strip()[:130]))
