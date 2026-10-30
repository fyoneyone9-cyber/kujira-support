# -*- coding: utf-8 -*-
"""DeliveryItem 型に last_imported_at を追加する。
DBには存在する列だが型に書かれていなかった。"""
import io

p = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
s = io.open(p, encoding="utf-8").read()
old = "  missing_in_last_import?: boolean | null"
if s.count(old) == 1:
    new = (old + "\n  // [LAST_IMPORT_FIX_V1] CSV取込日時。import-csv が毎回書く。\n"
                 "  last_imported_at?: string | null")
    s = s.replace(old, new, 1)
    print("added after missing_in_last_import")
else:
    old2 = "  p400_status?: string | null"
    assert s.count(old2) == 1, "fallback anchor not found"
    new2 = ("  // [LAST_IMPORT_FIX_V1] CSV取込日時。import-csv が毎回書く。\n"
            "  last_imported_at?: string | null\n" + old2)
    s = s.replace(old2, new2, 1)
    print("added before p400_status")
io.open(p, "w", encoding="utf-8").write(s)
