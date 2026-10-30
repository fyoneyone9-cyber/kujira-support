# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V11 2026-10-29] 自動入力が効かない真因を修正。

実測ログ:
    行3 label="1" -> ×
    行4 label="2" -> ×
  必須確認②は A列に No. があるため、vals.find() が最初に拾うのが
  設問名ではなく「1」「2」という**番号**だった。
  そのため fill のキーと一度も照合できていなかった。

対策: ラベル判定を「最も長いテキスト」にする。
      番号(数字のみ)や記号は除外し、実際の設問文を拾う。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_v11_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """        const label = vals.find(v => v && v !== '□' && v !== '✔') || ''"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)
NEW = """        // [HEARING_XLSX_V11 2026-10-29] A列に No. があるシート(必須確認②等)では
        //   先頭セルが「1」「2」という番号になり、設問名と照合できなかった。
        //   番号や記号を除き、最も長いテキストを設問名とみなす。
        const label = vals
          .filter(v => v && v !== '□' && v !== '✔' && !/^[0-9０-９.\\s]+$/.test(v))
          .sort((a, b) => b.length - a.length)[0] || ''"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
