# -*- coding: utf-8 -*-
"""[APPLICATION_PARSE_V3 2026-10-29] 契約者情報の抽出を修正。

V2の問題: blockValues が「右ブロック(費用明細)の文字列まで」拾っていた。
  1行の中に 左=契約者情報 / 右=費用明細 が同居しているため、
  7列目以降を全部見ると費用明細が混ざる。

対策: 左ブロックは **7〜36列** に限定する。
  実測で確認:
    契約者名  7〜22列
    住所      7〜36列
    費用明細  40列以降
  40列より手前で切れば混ざらない。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\parse-application\route.ts"
shutil.copy2(P, P + ".bak_v3_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """      for (const cs of Object.keys(r).map(Number).sort((a, b) => a - b)) {
        if (cs < 7) continue"""
assert s.count(OLD) == 1, "anchor1"
NEW = """      for (const cs of Object.keys(r).map(Number).sort((a, b) => a - b)) {
        // [V3] 左ブロックは 7〜36列。40列以降は費用明細なので混ぜない。
        if (cs < 7 || cs >= COL_NAME) continue"""
s = s.replace(OLD, NEW, 1)

OLD2 = """      const li = cols.find(c => tag.test(r[c]))
      if (li === undefined) continue
      const after = cols.filter(c => c > li).map(c => r[c]).filter(v => !tag.test(v))"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """      const li = cols.find(c => c < COL_NAME && tag.test(r[c]))
      if (li === undefined) continue
      const after = cols.filter(c => c > li && c < COL_NAME)
        .map(c => r[c]).filter(v => !tag.test(v))"""
s = s.replace(OLD2, NEW2, 1)

# 納品希望日も左ブロックに限定
OLD3 = """    for (const c of Object.keys(r).map(Number).sort((a, b) => a - b)) {
      const v = r[c]
      if (!v || seen.has(v)) continue
      seen.add(v)
      seq.push(v)
    }"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """    for (const c of Object.keys(r).map(Number).sort((a, b) => a - b)) {
      if (c >= COL_NAME) continue           // [V3] 費用明細を混ぜない
      const v = r[c]
      if (!v || seen.has(v)) continue
      seen.add(v)
      seq.push(v)
    }"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
