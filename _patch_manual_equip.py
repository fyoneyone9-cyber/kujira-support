# -*- coding: utf-8 -*-
"""[MANUAL_EQUIP_STATUS_V1 2026-10-29]
CSV再取込で P400/PayCube/VEGA3000 の手配状況が「未発注」に戻る問題の修正。

原因: 012の方針では「CSV由来の列=毎回上書き / ダッシュボード専用列=importが触らない」
      と分離していたが、011で追加した p400_status 等は CSV由来の列なのに
      UI が手動入力をそこへ書き込んでいた。import が毎回CSV値(空欄含む)で潰す。
対策: 手動値を *_manual 専用カラムへ分離。表示は「手動優先、無ければCSV値」。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_manualequip_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak); print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# ---- 1) 型定義に manual カラムを追加
OLD_T = "  p400_status?: string | null"
assert s.count(OLD_T) == 1, "type anchor"
NEW_T = """  p400_status?: string | null
  // [MANUAL_EQUIP_STATUS_V1] ダッシュボードで手動設定した手配状況。
  //   *_status はCSV由来でimportに毎回上書きされるため、手動値はこちらに保存する。
  p400_status_manual?: string | null
  paycube_status_manual?: string | null
  vega3000_status_manual?: string | null"""
s = s.replace(OLD_T, NEW_T, 1)

# ---- 2) 読み: 手動優先 / 書き: manual列へ
OLD_G = """            const getStatus = (name: string) => {
              if (name === 'P400')    return it.p400_status || null
              if (name === 'PayCube') return it.paycube_status || null
              // PayPay/キーボックス等はdashboard_todosに保存
              return (it.dashboard_todos?.[statusKey(name)] as string) || null
            }
            const getField = (name: string) => {
              if (name === 'P400')    return 'p400_status'
              if (name === 'PayCube') return 'paycube_status'
              return null // PayPay等はsaveTodoKey経由
            }"""
assert s.count(OLD_G) == 1, "getStatus anchor"
NEW_G = """            // [MANUAL_EQUIP_STATUS_V1 2026-10-29] 手動値を最優先、無ければCSV値。
            //   以前は読み書き両方が p400_status(CSV由来列)を共有していたため、
            //   CSV再取込で手動の「発注済み」等が空に潰され「未発注」に戻っていた。
            const getStatus = (name: string) => {
              if (name === 'P400')     return it.p400_status_manual || it.p400_status || null
              if (name === 'PayCube')  return it.paycube_status_manual || it.paycube_status || null
              if (name === 'VEGA3000') return it.vega3000_status_manual || it.vega3000_status || null
              // PayPay/キーボックス等はdashboard_todosに保存
              return (it.dashboard_todos?.[statusKey(name)] as string) || null
            }
            // 書き込み先は必ず *_manual。CSV由来列には絶対に書かないこと(再取込で消える)。
            const getField = (name: string) => {
              if (name === 'P400')     return 'p400_status_manual'
              if (name === 'PayCube')  return 'paycube_status_manual'
              if (name === 'VEGA3000') return 'vega3000_status_manual'
              return null // PayPay等はsaveTodoKey経由
            }"""
s = s.replace(OLD_G, NEW_G, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("page.tsx patched")

# ---- 3) import-csv 側に「manual列は触らない」ガードコメント+明示除外
Q = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\import-csv\route.ts"
bak2 = Q + ".bak_manualequip_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(Q, bak2); print("backup:", bak2)
t = io.open(Q, encoding="utf-8").read()
OLD_C = """    // 長納期機器の手配状況（例：発注済み/未発注/納品済み 等が入っている想定）"""
assert t.count(OLD_C) == 1, "csv anchor"
NEW_C = """    // 長納期機器の手配状況（例：発注済み/未発注/納品済み 等が入っている想定）
    // [MANUAL_EQUIP_STATUS_V1 2026-10-29] これらは「CSV由来の列」。毎回上書きされる。
    //   ダッシュボードで手動設定した値は p400_status_manual 等の専用列に入っており、
    //   ここでは一切触らないので再取込しても保持される。
    //   ⚠ UIから *_status(CSV列)へ手動値を書き込まないこと(再取込で必ず消える)。"""
t = t.replace(OLD_C, NEW_C, 1)
io.open(Q, "w", encoding="utf-8").write(t)
print("route.ts patched")
