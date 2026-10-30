# -*- coding: utf-8 -*-
"""[HEARING_GAS_V18 2026-10-29] 新構成に合わせてキーワード表を更新する。

新構成(14シート):
  PMS / カードキー / シリンダー錠 / スマホカード決済 / スマートロック①③ /
  プリンタ / 事前チェックイン / 工事 / 必須確認①②③ / 現金決済 / 端末カード決済

廃止: スマートロック② / PayPay決済 / ルームタブレット /
      フロントチェックイン / デイユース / 補助金
新設: スマートロック③ / 工事
"""
import io, shutil, datetime

# ---- GAS ----
P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(P, P + ".bak_v18_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
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
  printer:    ['プリンタ'],
  precheckin: ['事前チェックイン'],
  koji:       ['工事']
};"""
s = s[:i] + NEW + s[j:]
io.open(P, "w", encoding="utf-8").write(s)
print("GAS: キーワード表を更新（paypay/roomtablet を削除、koji を追加）")

# ---- page.tsx ----
P2 = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P2, P2 + ".bak_v18_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
t = io.open(P2, encoding="utf-8").read()

old = """                                      if (hasTablet) equips.push('roomtablet')"""
assert t.count(old) == 1, "anchor roomtablet: %d" % t.count(old)
t = t.replace(old, "", 1)

old2 = """                                      equips.push('sumaho')
                                      equips.push('paypay')"""
assert t.count(old2) == 1, "anchor sumaho: %d" % t.count(old2)
new2 = """                                      equips.push('sumaho')
                                      // [V18] 工事シートは新設。判断材料が無いので常にONにしておく
                                      equips.push('koji')"""
t = t.replace(old2, new2, 1)
io.open(P2, "w", encoding="utf-8").write(t)
print("page.tsx: roomtablet/paypay を削除、koji を追加")
