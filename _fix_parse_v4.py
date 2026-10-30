# -*- coding: utf-8 -*-
"""[APPLICATION_PARSE_V4 2026-10-29] 重複と誤抽出を潰す。

残課題:
 (1) 住所が「〒160-0022 東京都…」×9回 と重複
     → ブロック内の行をまたいだ重複除去をしていなかった（行単位でしか見ていない）
 (2) client が「●初期費用」になる
     → ①契約者名 ブロックの行に、右ブロックの見出し「●初期費用」が39列にある。
       COL_NAME(40)未満なので弾けていなかった。左ブロックは 36列まで。
 (3) contact が空
     → ④担当者氏名 ブロックから、カナでも数字でもメールでもない値を選ぶ条件が
       厳しすぎた（「石川　泰裕」は全角スペース入り）。先頭2件から選ぶ方式にする。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\parse-application\route.ts"
shutil.copy2(P, P + ".bak_v4_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

# (1)(2) blockValues を作り直す
i = s.index("  /** 指定ブロック内で、ラベル(TEL等)でない「値」を集める */")
j = s.index("  /** ブロック内で特定ラベルの右隣にある値 */")
NEW = """  /**
   * 指定ブロック内の「値」を集める。
   * [V4] 列は 7〜36 に限定（37列以降は右ブロックの見出しが入る）。
   *      ブロック全体で重複を除く（横方向の結合で同じ値が何十列も並ぶため）。
   */
  const blockValues = (labelRe: RegExp) => {
    const out: string[] = []
    const seen = new Set<string>()
    for (const ri of blockRows(labelRe)) {
      const r = grid[ri]
      for (const cs of Object.keys(r).map(Number).sort((a, b) => a - b)) {
        if (cs < 7 || cs > 36) continue
        const v = r[cs]
        if (!v || seen.has(v)) continue
        seen.add(v)
        if (/^(TEL|FAX|メールアドレス|〒)$/.test(v)) continue
        if (/^[●○・※]/.test(v)) continue        // 右ブロックの見出し
        if (v.length < 2) continue
        out.push(v)
      }
    }
    return out
  }

"""
s = s[:i] + NEW + s[j:]

# labeledValue も 36列までに
s = s.replace("const li = cols.find(c => c < COL_NAME && tag.test(r[c]))",
              "const li = cols.find(c => c <= 36 && tag.test(r[c]))", 1)
s = s.replace("const after = cols.filter(c => c > li && c < COL_NAME)",
              "const after = cols.filter(c => c > li && c <= 36)", 1)
s = s.replace("      if (c >= COL_NAME) continue           // [V3] 費用明細を混ぜない",
              "      if (c > 36) continue                  // [V4] 費用明細を混ぜない", 1)

# (3) 担当者の選び方を緩める
OLD3 = """  const contactVals = blockValues(/^④担当者氏名/)
  const contact = contactVals.find(v => !/^[ァ-ヶー\\s　]+$/.test(v) && !/[\\d@]/.test(v)) || ''
  const contactKana = contactVals.find(v => /^[ァ-ヶー\\s　]+$/.test(v)) || ''"""
assert s.count(OLD3) == 1, "anchor contact"
NEW3 = """  // [V4] ④担当者氏名ブロックは「カナ → 漢字 → TEL → メール」の順に並ぶ。
  //   電話番号やメールを除いた先頭2件が カナ / 漢字。
  const contactVals = blockValues(/^④担当者氏名/)
    .filter(v => !/@/.test(v) && !/^[\\d\\-+() ]+$/.test(v))
  const isKana = (v: string) => /^[ァ-ヶー\\s　]+$/.test(v)
  const contact = contactVals.find(v => !isKana(v)) || ''
  const contactKana = contactVals.find(isKana) || ''"""
s = s.replace(OLD3, NEW3, 1)

# 住所は結合せず最初の1件
s = s.replace("  const clientAddress = addrVals.join(' ')",
              "  const clientAddress = addrVals.join(' ')   // 〒行と住所行が分かれているので連結", 1)
s = s.replace("  const siteAddress = siteVals.join(' ')",
              "  const siteAddress = siteVals.join(' ')", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
