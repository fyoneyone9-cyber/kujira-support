# -*- coding: utf-8 -*-
"""[MANUAL_EQUIP_STATUS_V2 2026-10-29] DDL不要版に差し替え。

V1案は *_manual カラム追加だったが、Supabaseへ DDL を流す経路が無い
(exec_migration等のRPC不在 / DBパスワード未保有)。
一方、既に dashboard_todos (jsonb) が「importが一切触らないダッシュボード専用列」
として存在し、PayPay/キーボックスはそこへ保存されている(getField→null→saveTodoKey)。
P400/PayCube も同じ経路に乗せれば DB変更ゼロで解決し、かつ
「手動入力はdashboard_todosに集約」という一本化にもなる。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_manualequip2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak); print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# ---- V1で入れた型定義を整理(manualカラムは使わないので撤去)
OLD_T = """  p400_status?: string | null
  // [MANUAL_EQUIP_STATUS_V1] ダッシュボードで手動設定した手配状況。
  //   *_status はCSV由来でimportに毎回上書きされるため、手動値はこちらに保存する。
  p400_status_manual?: string | null
  paycube_status_manual?: string | null
  vega3000_status_manual?: string | null"""
assert s.count(OLD_T) == 1, "type anchor v1"
s = s.replace(OLD_T, "  p400_status?: string | null", 1)

# ---- 読み書きを dashboard_todos へ一本化
OLD_G = """            // [MANUAL_EQUIP_STATUS_V1 2026-10-29] 手動値を最優先、無ければCSV値。
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
assert s.count(OLD_G) == 1, "getStatus anchor v1"
NEW_G = """            // [MANUAL_EQUIP_STATUS_V2 2026-10-29] 手動の手配状況は dashboard_todos に保存する。
            //   【不具合】CSV再取込でP400の「発注済み」等が「未発注」に巻き戻っていた。
            //   【原因】読み書き両方が p400_status / paycube_status を使っていたが、
            //           これは「CSV由来の列」でimport-csvが毎回CSV値(空欄含む)で上書きする。
            //           migration 012 の方針どおり、手動入力は import が触らない列に置く必要がある。
            //   【対策】PayPay/キーボックスと同じ dashboard_todos 経路へ一本化。
            //           表示は「手動値 > CSV値」。CSV列は参考値としての表示にのみ使う。
            //   ⚠ 手動値を *_status(CSV由来列)へ書き戻さないこと。再取込で必ず消える。
            const getStatus = (name: string) => {
              const manual = (it.dashboard_todos?.[statusKey(name)] as string) || null
              if (manual) return manual
              if (name === 'P400')     return it.p400_status || null
              if (name === 'PayCube')  return it.paycube_status || null
              if (name === 'VEGA3000') return it.vega3000_status || null
              return null
            }
            // null を返す = saveTodoKey(dashboard_todos) 経路に乗る。
            // ここで列名を返すと patch() がCSV由来列を直接書いてしまうので返さない。
            const getField = (_name: string): string | null => null"""
s = s.replace(OLD_G, NEW_G, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("page.tsx patched (V2 / no DDL)")

# ---- マイグレーションは適用しないので .skip に退避
import os
M = r"C:\GensparkClaw\kujira-support\supabase\migrations\024_delivery_items_manual_equip_status.sql"
if os.path.exists(M):
    os.rename(M, M + ".notapplied")
    print("migration 024 -> .notapplied (V2ではDDL不要)")
