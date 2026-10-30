# -*- coding: utf-8 -*-
"""[MANUAL_DUEDATE_V1 2026-10-29] 画面で直した納品予定日が再取込で巻き戻る問題の修正。

監査(_audit_overwrite.js)で判明:
  import-csv が毎回上書きする列 ∩ UIが手動で書く列 = { status, delivery_due_date }
  - status は「既に手動doneなら維持」ガードが既にある(10/27対応済み)      → 安全
  - delivery_due_date は【ガードが一切無い】                              → 🔴毎回CSV値に戻る
    page.tsx L1753 で納期を手入力できるのに、再取込で必ず元に戻っていた。

方針(migration 012 と同じ):
  手動で変更した納期は dashboard_todos.manual_due_date に保存し、
  import は「手動値があればそれを優先」する。dashboard_todos は import が
  触らない列なので再取込しても消えない。DDL不要。
"""
import io, shutil, datetime

# ---------------------------------------------------------------- import 側
Q = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\import-csv\route.ts"
bak = Q + ".bak_duedate_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(Q, bak); print("backup:", bak)
t = io.open(Q, encoding="utf-8").read()

OLD1 = """  const { data: existingRows } = await supabase
    .from('delivery_items')
    .select('item_key, status')
  const existingStatusMap = new Map<string, string>()
  for (const row of existingRows || []) {
    existingStatusMap.set(row.item_key, row.status)
  }"""
assert t.count(OLD1) == 1, "imp anchor1"
NEW1 = """  const { data: existingRows } = await supabase
    .from('delivery_items')
    .select('item_key, status, dashboard_todos')
  const existingStatusMap = new Map<string, string>()
  // [MANUAL_DUEDATE_V1 2026-10-29] ダッシュボードで手動変更した納品予定日。
  //   画面(L1753付近)で納期を直せるのに、従来はCSV値で毎回上書きされ巻き戻っていた。
  //   手動値は dashboard_todos.manual_due_date にあり import は触らないので、
  //   ここで読み出して「手動値があればCSVより優先」する。
  const manualDueMap = new Map<string, string>()
  for (const row of existingRows || []) {
    existingStatusMap.set(row.item_key, row.status)
    const md = (row.dashboard_todos || {})['manual_due_date']
    if (md) manualDueMap.set(row.item_key, String(md))
  }"""
t = t.replace(OLD1, NEW1, 1)

OLD2 = """    const hashSrc = `${client_name}|${install_address}|${product_name}|${delivery_due_date}`"""
assert t.count(OLD2) == 1, "imp anchor2"
NEW2 = """    // [MANUAL_DUEDATE_V1] 手動で直した納期があればそちらを採用(CSVより優先)
    const manualDue = manualDueMap.get(item_key)
    const final_due_date = manualDue || delivery_due_date

    const hashSrc = `${client_name}|${install_address}|${product_name}|${delivery_due_date}`"""
t = t.replace(OLD2, NEW2, 1)

OLD3 = "      delivery_due_date, delivery_date,"
assert t.count(OLD3) == 1, "imp anchor3"
NEW3 = "      delivery_due_date: final_due_date, delivery_date,   // [MANUAL_DUEDATE_V1] 手動値優先"
t = t.replace(OLD3, NEW3, 1)

io.open(Q, "w", encoding="utf-8").write(t)
print("import-csv patched")

# ---------------------------------------------------------------- UI 側
P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak2 = P + ".bak_duedate_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak2); print("backup:", bak2)
s = io.open(P, encoding="utf-8").read()

OLD4 = ("onBlur={(e) => { if (e.target.value && e.target.value !== it.delivery_due_date) "
        "patch(it.id, { delivery_due_date: e.target.value }) }}")
assert s.count(OLD4) == 1, "ui anchor"
NEW4 = ("onBlur={(e) => { if (e.target.value && e.target.value !== it.delivery_due_date) {\n"
        "                        /* [MANUAL_DUEDATE_V1 2026-10-29] 納期はCSV由来列なので、手動値は\n"
        "                           dashboard_todos にも残す。これが無いと再取込でCSV値に巻き戻る。 */\n"
        "                        patch(it.id, { delivery_due_date: e.target.value })\n"
        "                        saveTodoKey(it.id, it.dashboard_todos, 'manual_due_date', e.target.value)\n"
        "                      } }}")
s = s.replace(OLD4, NEW4, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("page.tsx patched")
