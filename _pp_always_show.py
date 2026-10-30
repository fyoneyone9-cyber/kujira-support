# -*- coding: utf-8 -*-
"""[PAYPAY_APPLY_LOG_V2 2026-10-30] PayPay欄が表示されない問題を修正。

症状:「どこにあんの？みえねえけど」

真因: `name === 'PayPay'` の機材ブロック内に置いていたが、
  実データ411件を調べたところ **PayPayという機材名は1件も存在しない**。
  （機材名は P400 / PayCube / VEGA3000 / スマートロック … など）
  そのため表示条件を一度も満たしていなかった。

対策: 機材ブロックから切り離し、カード内に常時表示する。
  PayPayは「機材」ではなく「契約手続き」なので、機材構成とは独立している。
  申込書に PayPay があればその旨も出す。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_ppshow_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
L = io.open(P, encoding="utf-8").read().split("\n")

# 挿入したブロックを探して切り出す
st = None
for i, l in enumerate(L):
    if "PAYPAY_APPLY_LOG_V1 2026-10-29] 申請の有無と日付" in l:
        st = i
        break
assert st is not None, "ブロックが見つからない"
en = st
depth = 0
started = False
for i in range(st, len(L)):
    if "{(() => {" in L[i]:
        started = True
    if started and L[i].strip() == "})()}":
        en = i + 1
        break
assert en > st, "終端が見つからない"
block = L[st:en]
print("既存ブロック: L%d-%d (%d行)" % (st + 1, en, len(block)))
del L[st:en]

# お客様メール欄の直前に移動する（カード内で常に表示される位置）
tgt = None
for i, l in enumerate(L):
    if "CLIENT_EMAIL_V1 2026-10-29] お客様メールアドレス" in l:
        tgt = i
        break
assert tgt is not None, "挿入先が見つからない"

# インデントを合わせる
new_indent = len(L[tgt]) - len(L[tgt].lstrip())
old_indent = len(block[0]) - len(block[0].lstrip())
diff = new_indent - old_indent
adj = []
for b in block:
    if not b.strip():
        adj.append(b)
    elif diff > 0:
        adj.append(" " * diff + b)
    else:
        adj.append(b[-diff:] if b[:-diff].strip() == "" else b)

# 見出しを変更（機材欄ではなくなるため）
adj = [x.replace("PAYPAY_APPLY_LOG_V1 2026-10-29] 申請の有無と日付",
                 "PAYPAY_APPLY_LOG_V2 2026-10-30] PayPay申請の有無と日付。"
                 "機材名に PayPay が無いため機材欄ではなく常時表示する") for x in adj]

L[tgt:tgt] = adj
io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("L%d に移動（常時表示）" % (tgt + 1))
