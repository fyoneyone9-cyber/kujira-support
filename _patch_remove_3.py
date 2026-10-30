# -*- coding: utf-8 -*-
"""[HEARING_SHEET_BUILDER_V5 2026-10-29]
ユーザー指示「デイユース / 工事 / IT導入補助金はいらない」に従い、
V1で追加した3つの【要確認】シートを判定から外す。

経緯: 社内フローチャートには分岐が存在するが、実運用では不要とのこと。
      雛形CSVもDLされていない(= 実際には使われていない)ことと整合する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_rm3_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                    // [HEARING_SHEET_BUILDER_V1] 社内フローチャートにある分岐のうち、
                    //   機材情報だけでは判定できないもの。ヒアリングで確認する前提で候補に出す。
                    { label: 'デイユース', reason: '日帰り利用がある場合（要確認）' },
                    { label: '工事', reason: 'LANケーブル・電源が設置不可の場合（要確認）' },
                    { label: 'IT導入補助金', reason: '補助金を利用する場合（要確認）' },
"""
assert s.count(OLD) == 1, "anchor"
NEW = """                    // [HEARING_SHEET_BUILDER_V5 2026-10-29] デイユース / 工事 / IT導入補助金は
                    //   社内フローチャートには分岐があるが、実運用では使わないとのユーザー指示により除外。
                    //   （雛形CSVも配布されていないことと整合）
"""
s = s.replace(OLD, NEW, 1)

# 【要確認】に関するプロンプト条項も不要になるので調整
OLD2 = """【8】「（要確認）」と書かれたシートは該当するか不明なため、
　　シート名の先頭に【要確認】を付けて最後にまとめ、
　　表紙に「該当しない場合は削除してください」と注記する。

"""
if OLD2 in s:
    s = s.replace(OLD2, "", 1)
    print("removed rule 8")
    # 番号を詰める
    s = s.replace("【9】先頭に「表紙」シートを作り", "【8】先頭に「表紙」シートを作り", 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
