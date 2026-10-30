# -*- coding: utf-8 -*-
"""[HEARING_AUTOFILL_V1 2026-10-29] 案件情報をヒアリングシートに自動入力する。

これまで prefill は「必須確認①のチェックボックス」しか見ておらず、
会社名・住所・担当者などのテキスト項目が空のままだった。

必須確認②の構造（調査結果）:
  行3  B列「組織名(会社名)」
  行6  B列「DMSにログインされる方のお名前」
  行8  B列「物件名」
  行13 B列「物件の住所」
  行14 B列「物件の郵便番号」
  → 回答欄はC列以降（□が無い行は空セルに直接書く）

対策: 「項目名で照合 → 同じ行の回答欄に値を書く」汎用ロジックを入れる。
      行番号を決め打ちしないので、雛形が変わっても追従する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_autofill_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# Body 型に fill を追加
OLD_T = """type Body = {
  sheets: string[]                       // 作成するシート名（順番どおり）
  info?: Record<string, string>          // 表紙に載せる案件情報
  prefill?: Record<string, string>       // 必須確認①などの事前チェック内容
}"""
assert s.count(OLD_T) == 1, "type anchor"
NEW_T = """type Body = {
  sheets: string[]                       // 作成するシート名（順番どおり）
  info?: Record<string, string>          // 表紙に載せる案件情報
  prefill?: Record<string, string>       // 必須確認①などの事前チェック内容
  // [HEARING_AUTOFILL_V1] 項目名 -> 入れる値。項目名で行を探して回答欄に書く。
  fill?: Record<string, string>
}"""
s = s.replace(OLD_T, NEW_T, 1)

OLD_P = "  const prefill = body.prefill || {}"
assert s.count(OLD_P) == 1, "prefill anchor"
NEW_P = """  const prefill = body.prefill || {}
  // [HEARING_AUTOFILL_V1 2026-10-29] 案件情報の自動入力。
  //   「項目名を含むセル」を探し、その行の回答欄へ値を書く。
  //   行番号を決め打ちしないので雛形が変わっても追従する。
  const fill = body.fill || {}"""
s = s.replace(OLD_P, NEW_P, 1)

# 行描画の直後に自動入力を差し込む
OLD_ROW = """      const r = ws.addRow(vals)
      r.alignment = { wrapText: true, vertical: 'middle' }"""
assert s.count(OLD_ROW) == 1, "row anchor"
NEW_ROW = """      // [HEARING_AUTOFILL_V1] この行の項目名が fill のキーと一致したら回答欄に値を入れる
      {
        const label = vals.find(v => v && v !== '□' && v !== '✔') || ''
        if (label) {
          const key = Object.keys(fill).find(k => label.includes(k))
          if (key && fill[key]) {
            // 回答欄の位置: □があればそこ、無ければ L列(ANS) に書く
            let target = vals.findIndex(v => v === '□')
            if (target < 0) target = ANS - 1
            while (vals.length <= target) vals.push('')
            vals[target] = fill[key]
          }
        }
      }

      const r = ws.addRow(vals)
      r.alignment = { wrapText: true, vertical: 'middle' }"""
s = s.replace(OLD_ROW, NEW_ROW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
