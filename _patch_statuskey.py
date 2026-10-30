# -*- coding: utf-8 -*-
"""[MANUAL_EQUIP_STATUS_V2] dashboard_todos のキー名を manual_ プレフィクスで明確化。
statusKey('P400') が 'p400_status' を返すと、CSV由来カラム p400_status と同名になり
将来の取り違え事故を招くため。"""
import io

p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(p, encoding="utf-8").read()

old = ("            const statusKey = (name: string) => "
       "name === '\u30ad\u30fc\u30dc\u30c3\u30af\u30b9' ? 'keybox_status' : "
       "`${name.toLowerCase()}_status`")
assert s.count(old) == 1, "statusKey anchor"

new = """            // [MANUAL_EQUIP_STATUS_V2] dashboard_todos 内のキー名。
            //   P400/PayCube/VEGA3000 は同名のCSV由来カラム(p400_status等)が別に存在する。
            //   同名だと「どちらを読んでいるか」を将来必ず取り違えるので manual_ を付けて分離する。
            const CSV_BACKED = ['P400', 'PayCube', 'VEGA3000']
            const statusKey = (name: string) =>
              name === '\u30ad\u30fc\u30dc\u30c3\u30af\u30b9' ? 'keybox_status'
              : CSV_BACKED.includes(name) ? `manual_${name.toLowerCase()}_status`
              : `${name.toLowerCase()}_status`"""

s = s.replace(old, new, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("statusKey patched")
