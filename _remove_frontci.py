# -*- coding: utf-8 -*-
"""[HEARING_GAS_V16 2026-10-29] フロントチェックインを完全に削除する。

指示:「フロントチェックイン いらない シートごと削除した」
  ユーザーが自分のマスターシートから該当シートを削除済み。
  コード側に残っていると「存在しないシートを残す」判定が走って無駄なので全部外す。

対象:
  (1) hearing-gas.js      EQUIP_SHEETS から frontci を削除
  (2) hearing-gas-dialog  チェックボックスを削除
  (3) page.tsx            設定コピーの equips から frontci を削除
  (4) hearingSheetDefs.ts 定義からも削除（Excel側は撤去済みだが残骸を消す）
"""
import io, shutil, datetime, json, re

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------- (1) hearing-gas.js ----------
P1 = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(P1, P1 + ".bak_nofront_" + ts)
s = io.open(P1, encoding="utf-8").read()
old = "  frontci:    ['\u30d5\u30ed\u30f3\u30c8\u30c1\u30a7\u30c3\u30af\u30a4\u30f3'],\n"
assert s.count(old) == 1, "gas anchor: %d" % s.count(old)
s = s.replace(old, "", 1)
io.open(P1, "w", encoding="utf-8").write(s)
print("(1) hearing-gas.js: frontci 削除")

# ---------- (2) dialog ----------
P2 = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
shutil.copy2(P2, P2 + ".bak_nofront_" + ts)
d = io.open(P2, encoding="utf-8").read()
# チェックボックスの行ごと削除
d2 = re.sub(r'\s*<div class="chk"><input type="checkbox" id="chk_frontci"[^>]*>'
            r'<label for="chk_frontci">[^<]*</label></div>', "", d)
assert d2 != d, "dialog checkbox not found"
d = d2
# KEYS から外す
d = d.replace("'precheckin','frontci'", "'precheckin'")
# 注記からも外す
d = d.replace("PayPay\u6c7a\u6e08 / \u30b9\u30de\u30db\u30ab\u30fc\u30c9\u6c7a\u6e08 / \u30d5\u30ed\u30f3\u30c8\u30c1\u30a7\u30c3\u30af\u30a4\u30f3 \u306f",
              "PayPay\u6c7a\u6e08 / \u30b9\u30de\u30db\u30ab\u30fc\u30c9\u6c7a\u6e08 \u306f")
io.open(P2, "w", encoding="utf-8").write(d)
print("(2) dialog: チェックボックスとKEYSから削除")

# ---------- (3) page.tsx ----------
P3 = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P3, P3 + ".bak_nofront_" + ts)
t = io.open(P3, encoding="utf-8").read()
old3 = "                                      equips.push('frontci')\n"
assert t.count(old3) == 1, "page anchor: %d" % t.count(old3)
t = t.replace(old3, "", 1)
io.open(P3, "w", encoding="utf-8").write(t)
print("(3) page.tsx: equips から削除")

# ---------- (4) hearingSheetDefs.ts ----------
P4 = r"C:\GensparkClaw\kujira-support\src\lib\hearingSheetDefs.ts"
shutil.copy2(P4, P4 + ".bak_nofront_" + ts)
raw = io.open(P4, encoding="utf-8").read()
head, body = raw.split("= ", 1)
defs = json.loads(body.strip())
key = "\u30d5\u30ed\u30f3\u30c8\u30c1\u30a7\u30c3\u30af\u30a4\u30f3"
if key in defs:
    del defs[key]
    io.open(P4, "w", encoding="utf-8").write(
        head + "= " + json.dumps(defs, ensure_ascii=False, indent=1) + "\n")
    print("(4) hearingSheetDefs.ts: 削除。残り %d シート" % len(defs))
else:
    print("(4) hearingSheetDefs.ts: 元々なし")
