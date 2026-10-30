# -*- coding: utf-8 -*-
"""[KOUTEI_GAS_V3 2026-10-29] 行削除ロジックのバグを修正。

症状: チェックを外したキーボックス等の工程が残る。

真因: 連続行をまとめる while ループが壊れていた。
  var i2 = del.length - 1;
  while (i2 >= 0) {
    var end = del[i2], start = end;
    while (i2 > 0 && del[i2-1] === start - 1) { i2--; start = del[i2]; }
    sh.deleteRows(start, end - start + 1);
    i2--;                                   // ← ここで余分に1つ飛ばす
  }
  内側のループで i2 を減らした後、外側でさらに i2-- するため
  1行おきに削除対象を取りこぼしていた。

対策: まとめ処理をやめ、**下から1行ずつ確実に削除**する。
  行数はたかだか100行程度なので速度より確実性を優先する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\koutei-gas.js"
shutil.copy2(P, P + ".bak_v3_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

i = s.index("  // \u524a\u9664\u5bfe\u8c61\u306e\u884c\u3092\u96c6\u3081\u308b")
j = s.index("  // \u6848\u4ef6\u60c5\u5831\u3092\u5dee\u3057\u8fbc\u3080")

NEW = """  // [V3] 削除対象の行番号を集める（1始まり）
  //   区分が空の行はヘッダや区切りなので残す。
  var del = [];
  for (var i = 3; i < vals.length; i++) {
    var c = String(vals[i][0] || '').trim();
    if (!c) continue;
    if (!keep[c]) del.push(i + 1);
  }

  // [V3] 下から1行ずつ確実に削除する。
  //   以前は連続行をまとめていたが、インデックス操作を誤って
  //   1行おきに取りこぼしていた（キーボックス等が残る原因）。
  //   100行程度なので速度より確実性を優先する。
  var removed = 0;
  for (var k = del.length - 1; k >= 0; k--) {
    sh.deleteRow(del[k]);
    removed++;
  }

"""
s = s[:i] + NEW + s[j:]
io.open(P, "w", encoding="utf-8").write(s)
print("削除ロジックを修正")
