# -*- coding: utf-8 -*-
"""[HEARING_SHEET_BUILDER_V4 2026-10-29]
抽出済みの設問定義(hearingSheetDefs.ts)をプロンプトに直接埋め込む。

V3までは雛形URLを渡すだけで、Geminiが実際にスプレッドシートを読めるかに依存していた。
V4は設問本文をプロンプトに同梱するので、URLを開けなくても正確なシートを作れる。
社内用の列は抽出時点で除去済み(_build_sheet_defs.py)。

未DLのシート(カードキー/現金決済/デイユース/工事/IT導入補助金)は定義が無いため、
その旨を明示して雛形から転記させる。黙って落とすと設問が欠ける。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_embeddefs_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# import 追加
OLD_IMP = "import { createClient } from '@/lib/supabase/client'"
if OLD_IMP in s:
    s = s.replace(OLD_IMP,
                  OLD_IMP + "\nimport { HEARING_SHEET_DEFS } from '@/lib/hearingSheetDefs'", 1)
    print("import added (client)")
else:
    # 先頭の import 群の最後に足す
    i = s.index("\n\n", s.index("import "))
    s = s[:i] + "\nimport { HEARING_SHEET_DEFS } from '@/lib/hearingSheetDefs'" + s[i:]
    print("import added (fallback)")

# プロンプトの「作成するシート」節に設問本文を同梱
OLD = """${hearingSheets.map((x, i) => `${i + 1}. ${x.label}  \u2190 ${x.reason}`).join('\\n')}"""
assert s.count(OLD) == 1, "anchor list"
NEW = """${hearingSheets.map((x, i) => `${i + 1}. ${x.label}  \u2190 ${x.reason}`).join('\\n')}

\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
\u25a0 各シートの設問（社内用の列は除去済み・この内容をそのまま使うこと）
\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501
${hearingSheets.map(x => {
  const def = HEARING_SHEET_DEFS[x.label]
  if (!def) return `\u3010${x.label}\u3011\\n\uff08\u5b9a\u7fa9\u672a\u767b\u9332\uff09\u96db\u5f62\u30b9\u30d7\u30ec\u30c3\u30c9\u30b7\u30fc\u30c8\u306e\u300c${x.label}\u300d\u30b7\u30fc\u30c8\u3092\u305d\u306e\u307e\u307e\u8ee2\u8a18\u3057\u3066\u304f\u3060\u3055\u3044\u3002\u8a2d\u554f\u3092\u5275\u4f5c\u3057\u306a\u3044\u3053\u3068\u3002`
  return `\u3010${x.label}\u3011\\n` + def.map(row => '  ' + row.join(' | ')).join('\\n')
}).join('\\n\\n')}"""
s = s.replace(OLD, NEW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
