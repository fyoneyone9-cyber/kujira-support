# -*- coding: utf-8 -*-
"""[HEARING_GAS_V8c] 埋まらない項目を外し、実際に埋まるものだけ残す。

調査結果:
  PMS         … 「Beds24のAPIキー」等、製品ごとの認証情報。ダッシュボードには無い → 外す
  スマートロック①… 解除コードタイプ/鍵の有効時間。案件情報では決まらない → 外す
  必須確認③   … 部屋番号の一覧表（回答欄なし）。1行ずつの表なので自動入力に不向き → 外す

残すのは必須確認②(11)/カードキー(4)/PayPay決済(2) = 17箇所。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
bak = P + ".bak_plan_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """    '必須確認③': [
      ['お部屋の総数', p.rooms]
    ],
    'PMS': [
      ['PMSの名称', p.pms],
      ['ご利用のPMS', p.pms]
    ],
    'カードキー': ["""
assert s.count(OLD) == 1, "anchor1: %d" % s.count(OLD)
NEW = """    // PMS / スマートロック① は製品ごとのAPIキー等なので案件情報からは埋まらない。
    // 必須確認③ は部屋番号の一覧表（回答欄なし）なので対象外。
    'カードキー': ["""
s = s.replace(OLD, NEW, 1)

OLD2 = """    'PayPay決済': [
      ['お名前',        p.contact],
      ['メールアドレス', p.email]
    ],
    'スマートロック①': [
      ['メーカー', p.lockMaker]
    ]
  };"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """    'PayPay決済': [
      ['お名前',        p.contact],
      ['メールアドレス', p.email]
    ]
  };"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
