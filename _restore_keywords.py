# -*- coding: utf-8 -*-
"""[HEARING_GAS_V19 2026-10-29] 最終構成16シートに合わせてキーワードを戻す。

最終構成:
  PMS / PayPay決済 / カードキー / シリンダー錠 / スマホカード決済 /
  スマートロック①③ / プリンタ / ルームタブレット / 事前チェックイン /
  工事 / 必須確認①②③ / 現金決済 / 端末カード決済

V18で paypay と roomtablet を消してしまったので復活させる。
（DL途中の状態を見て判断したのが原因。構成変更時は全部揃ってから反映すること）
"""
import io, shutil, datetime

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# ---- GAS ----
P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(P, P + ".bak_v19_" + ts)
s = io.open(P, encoding="utf-8").read()
i = s.index("var EQUIP_KEYWORDS = {")
j = s.index("};", i) + 2
NEW = """var EQUIP_KEYWORDS = {
  pms:        ['PMS'],
  smartlock:  ['スマートロック'],      // ①③ の両方を拾う
  cardkey:    ['カードキー'],
  cylinder:   ['シリンダー'],
  cash:       ['現金'],
  p400:       ['端末カード'],
  sumaho:     ['スマホカード', 'スマートカード'],
  paypay:     ['PayPay', 'ペイペイ'],
  printer:    ['プリンタ'],
  roomtablet: ['ルームタブレット'],
  precheckin: ['事前チェックイン'],
  koji:       ['工事']
};"""
s = s[:i] + NEW + s[j:]
io.open(P, "w", encoding="utf-8").write(s)
print("GAS: paypay / roomtablet を復活（全12キー）")

# ---- page.tsx ----
P2 = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P2, P2 + ".bak_v19_" + ts)
t = io.open(P2, encoding="utf-8").read()

old = """                                      equips.push('sumaho')
                                      // [V18] 工事シートは新設。判断材料が無いので常にONにしておく
                                      equips.push('koji')"""
assert t.count(old) == 1, "anchor: %d" % t.count(old)
new = """                                      if (hasTablet) equips.push('roomtablet')
                                      equips.push('sumaho')
                                      equips.push('paypay')
                                      // [V19] 工事シートは判断材料が無いので常にONにしておく
                                      equips.push('koji')"""
t = t.replace(old, new, 1)
io.open(P2, "w", encoding="utf-8").write(t)
print("page.tsx: roomtablet / paypay を復活")
