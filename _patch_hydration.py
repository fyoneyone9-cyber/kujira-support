# -*- coding: utf-8 -*-
"""[HYDRATION_FIX_V1 2026-10-29] React error #418 (text content mismatch) の修正。

原因: 「最終取込」ブロックが SSR時 と ブラウザ時 で異なる文字列を描画していた。
  L800  const hoursAgo = (Date.now() - new Date(stats.lastImport).getTime()) / 3600000
  L807  new Date(stats.lastImport).toLocaleString('ja-JP', ...)
 ・Date.now() はサーバーとクライアントで値が違う
 ・toLocaleString はサーバー(UTC/環境ロケール)とブラウザ(JST)で結果が違う
 → ハイドレーション不一致で #418。

対策: マウント後にだけ時刻表示を描画する(`mounted` フラグ)。
      SSR時はプレースホルダを出し、クライアントで確定値に差し替える。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_hydration_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# --- 1) mounted フラグを追加 ---
OLD1 = "  const [stats, setStats] = useState<{ total: number; lastImport: string | null; progressAlertCount?: number } | null>(null)"
assert s.count(OLD1) == 1, "anchor stats"
NEW1 = (OLD1 + "\n"
        "  // [HYDRATION_FIX_V1 2026-10-29] 時刻表示はSSRとクライアントで必ずズレる\n"
        "  //   (Date.now() / toLocaleString のロケール差)。React #418 の原因だった。\n"
        "  //   マウント後にだけ描画して不一致を無くす。\n"
        "  const [mounted, setMounted] = useState(false)\n"
        "  useEffect(() => { setMounted(true) }, [])")
s = s.replace(OLD1, NEW1, 1)

# --- 2) 最終取込ブロックを mounted ガード ---
OLD2 = """          const hoursAgo = stats?.lastImport ? (Date.now() - new Date(stats.lastImport).getTime()) / 3600000 : null
          const isAlert = hoursAgo !== null && hoursAgo >= 24"""
assert s.count(OLD2) == 1, "anchor hoursAgo"
NEW2 = """          // [HYDRATION_FIX_V1] mounted 前は時刻計算をしない(SSRと差が出るため)
          const hoursAgo = (mounted && stats?.lastImport)
            ? (Date.now() - new Date(stats.lastImport).getTime()) / 3600000 : null
          const isAlert = hoursAgo !== null && hoursAgo >= 24"""
s = s.replace(OLD2, NEW2, 1)

OLD3 = """                {stats?.lastImport ? new Date(stats.lastImport).toLocaleString('ja-JP', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' }) : '...'}"""
assert s.count(OLD3) == 1, "anchor toLocaleString"
NEW3 = """                {mounted && stats?.lastImport
                  ? new Date(stats.lastImport).toLocaleString('ja-JP', { month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit' })
                  : '...'}"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
