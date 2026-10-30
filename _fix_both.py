# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V8 2026-10-29] 残り2点を修正。

(1) 自動入力が効かない
    必須確認②は回答欄に □ が無い（空セル）。
    → □が無い場合は「項目名セルの次の非空セルの手前」= 回答欄とみなす。
      具体的には、その行で最後にテキストがある列の次（=結合の外）に書く。
      シート毎に回答欄の列が違うので、ヘッダ行の『ご回答欄』の列位置を記憶して使う。

(2) 必須確認②の結合が崩れる
    原因: A列に No. があるため「A〜K結合」ではなく「B〜H結合」等になる必要がある。
    既存ロジックは『次のテキストの手前まで』なので本来これで正しいが、
    ご回答欄(I/J/K)まで巻き込んでいた。
    → ヘッダ行から『ご回答欄』の開始列を検出し、結合はその手前で必ず止める。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\api\delivery\hearing-xlsx\route.ts"
bak = P + ".bak_v8_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# --- ANS を固定値ではなくシートごとに検出する ---
OLD = """    const ANS = 12                                   // L列 = ご回答欄"""
assert s.count(OLD) == 1, "anchor ANS"
NEW = """    // [HEARING_XLSX_V8 2026-10-29] 回答欄の列はシートごとに違う。
    //   ヘッダ行の『ご回答欄』を探して、その列を回答欄の開始位置とする。
    //   見つからなければ従来どおり L列(12)。
    let ANS = 12
    for (const row of def.slice(0, 6)) {
      const idx = row.findIndex(c => c && c.includes('ご回答欄'))
      if (idx >= 0) { ANS = idx + 1; break }
    }"""
s = s.replace(OLD, NEW, 1)

# --- 自動入力: □が無い行は ANS 列に書く（既存ロジックを強化） ---
OLD2 = """            // 回答欄の位置: □があればそこ、無ければ L列(ANS) に書く
            let target = vals.findIndex(v => v === '□')
            if (target < 0) target = ANS - 1"""
assert s.count(OLD2) == 1, "anchor fill"
NEW2 = """            // [HEARING_XLSX_V8] 回答欄の位置を決める。
            //   □があればそこ。無ければ ANS 列（ヘッダの『ご回答欄』位置）。
            let target = vals.findIndex(v => v === '□')
            if (target < 0) target = ANS - 1"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
