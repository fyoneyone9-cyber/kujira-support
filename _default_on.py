# -*- coding: utf-8 -*-
"""[HEARING_GAS_V10 2026-10-29] 判断がつかない3項目をデフォルトONにする。

指示: PayPay決済 / フロントチェックイン / スマホカード決済 は
      機材構成から判定できないので既定でONにしておく。
      （不要ならダイアログで外せばよい。足りないより余分な方が安全）

対応箇所:
  (1) dialog.html のチェックボックスに checked を付ける
  (2) ダッシュボードの「設定をコピー」でも常に equips に含める
      → 貼り付けで反映したときにOFFにならないようにする
"""
import io, shutil, datetime

# ---- (1) dialog.html ----
P1 = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
bak1 = P1 + ".bak_defon_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P1, bak1)
s = io.open(P1, encoding="utf-8").read()

for k in ["sumaho", "paypay", "frontci"]:
    a = '<input type="checkbox" id="chk_%s">' % k
    b = '<input type="checkbox" id="chk_%s" checked>' % k
    assert s.count(a) == 1, "dialog anchor %s: %d" % (k, s.count(a))
    s = s.replace(a, b, 1)

# 注記を追加
OLD = """  <div class="hint">※ 必須確認①②③は常に残ります</div>"""
assert s.count(OLD) == 1, "hint anchor"
NEW = """  <div class="hint">※ 必須確認①②③は常に残ります</div>
  <div class="hint" style="color:#b8860b">※ PayPay決済 / スマホカード決済 / フロントチェックイン は
    機材構成から判断できないため既定でONです。不要ならチェックを外してください</div>"""
s = s.replace(OLD, NEW, 1)
io.open(P1, "w", encoding="utf-8").write(s)
print("dialog.html: 3項目を checked に")

# ---- (2) page.tsx の設定コピー ----
P2 = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak2 = P2 + ".bak_defon_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P2, bak2)
t = io.open(P2, encoding="utf-8").read()

OLD2 = """                                      if (hasSumaho) equips.push('sumaho')
                                      if (hasPaypay) equips.push('paypay')"""
assert t.count(OLD2) == 1, "page anchor: %d" % t.count(OLD2)
NEW2 = """                                      // [HEARING_GAS_V10 2026-10-29] この3つは機材構成から判断できないので常にON。
                                      //   不要ならダイアログ側で外す運用（足りないより余分な方が安全）
                                      equips.push('sumaho')
                                      equips.push('paypay')
                                      equips.push('frontci')"""
t = t.replace(OLD2, NEW2, 1)
io.open(P2, "w", encoding="utf-8").write(t)
print("page.tsx: 設定コピーでも常時ON")
