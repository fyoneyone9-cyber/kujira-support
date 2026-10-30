# -*- coding: utf-8 -*-
"""[HEARING_GAS_V9 2026-10-29] チェックが入らない真因を修正。

症状: 「✅反映しました（機材3件にチェック）」と出るのにチェックが付かない。

真因: **id の重複**。
  テキスト欄 <input id="pms">        （PMS名）
  チェック   <input id="pms" type=checkbox>（PMSシートを残すか）
  → getElementById('pms') は先に現れるテキスト欄を返すため、
    .checked = true を文字列入力欄に対して設定していた（無視される）。
  cardkeyMaker / lockMaker も同様の衝突。

対策: チェックボックス側の id を `chk_` プレフィクス付きに変更し、衝突をなくす。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
bak = P + ".bak_idfix_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

KEYS = ['pms', 'smartlock', 'cardkey', 'cylinder', 'cash', 'p400',
        'sumaho', 'paypay', 'printer', 'roomtablet', 'precheckin', 'frontci']

# チェックボックスの id / for を chk_ 付きに
n = 0
for k in KEYS:
    a = '<input type="checkbox" id="%s"' % k
    b = '<input type="checkbox" id="chk_%s"' % k
    if a in s:
        s = s.replace(a, b)
        n += 1
    a2 = 'for="%s">' % k
    b2 = 'for="chk_%s">' % k
    s = s.replace(a2, b2)
print("checkbox id renamed: %d" % n)

# JS 側の参照を chk_ 付きに
OLD = """  var on = [];
  KEYS.forEach(function(k){
    var v = !!(d.equips && d.equips.indexOf(k) >= 0);
    document.getElementById(k).checked = v;
    if(v) on.push(k);
  });"""
assert s.count(OLD) == 1, "anchor1"
NEW = """  // [V9] チェックボックスの id は chk_ 付き（テキスト欄との衝突を避けるため）
  var on = [];
  KEYS.forEach(function(k){
    var el = document.getElementById('chk_' + k);
    if(!el) return;
    var v = !!(d.equips && d.equips.indexOf(k) >= 0);
    el.checked = v;
    if(v) on.push(k);
  });"""
s = s.replace(OLD, NEW, 1)

OLD2 = """  var equips = KEYS.filter(function(k){ return document.getElementById(k).checked; });"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """  var equips = KEYS.filter(function(k){
    var el = document.getElementById('chk_' + k);
    return el && el.checked;
  });"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")

# 検証: id重複が無いか
ids = re.findall(r'id="([^"]+)"', s)
dup = set(x for x in ids if ids.count(x) > 1)
print("重複id:", dup if dup else "なし ← 正常")
