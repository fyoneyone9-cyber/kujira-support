# -*- coding: utf-8 -*-
"""[LAST_IMPORT_FIX_V1 2026-10-29]
症状:「取り込み実施してるのに『最終取込 10/27 / 52時間未取込』のまま反映されない」

実データ確認(読み取りのみ):
  last_imported_at 最新 = 2026-10-29T08:12:03Z (= 日本時間 17:12)
  日付別: 10/20=2, 10/22=22, 10/24=1, 10/27=7, 10/29=379
  → **取り込みは成功している**。表示だけが古い。

真因: delivery/page.tsx L477
    const lastImport = all.reduce((a,b) => a.created_at > b.created_at ? a : b).created_at
  **`created_at`(レコード作成日時)を見ていた**。
  import-csv は upsert なので既存行の created_at は更新されない。
  新規行が増えた日(=10/27)が「最終取込」として表示され続けていた。
  正しくは import-csv が毎回書いている `last_imported_at` を見るべき。

同じ誤りが paycube/page.tsx L117 にもあるか確認して直す。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_lastimport_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = ("    const lastImport = all.length > 0 ? "
       "all.reduce((a, b) => a.created_at > b.created_at ? a : b).created_at : null")
assert s.count(OLD) == 1, "anchor delivery: %d" % s.count(OLD)
NEW = ("""    // [LAST_IMPORT_FIX_V1 2026-10-29] created_at(レコード作成日時)ではなく
    //   last_imported_at(取込日時)を見る。import-csv は upsert なので
    //   既存行の created_at は更新されず、「最終取込」が何日も古いまま表示されていた。
    const lastImport = all.length > 0
      ? (all.map(x => x.last_imported_at).filter(Boolean).sort().slice(-1)[0] || null)
      : null""")
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("delivery patched")

# --- paycube 側も確認 ---
Q = r"C:\GensparkClaw\kujira-support\src\app\(app)\paycube\page.tsx"
t = io.open(Q, encoding="utf-8").read()
L = t.split("\n")
print("\npaycube L115-121:")
for i in range(115, 122):
    print("  %d| %s" % (i, L[i - 1].rstrip()[:140]))
