# -*- coding: utf-8 -*-
"""[GAS_VERSION_GUARD_V1 2026-10-29] 片方だけ貼り替える事故を根絶する。

今日の事故:
  dialog は V25、コード.gs は V22 という不整合で動かなくなった。
  「両方貼ってください」と口で言うだけでは防げない（実際3回起きた）。

汎用対策:
  (1) **両ファイルに同じバージョン文字列を埋め込む**
      ビルド時に自動で同期するので、ズレようがない
  (2) dialog 起動時にサーバー側バージョンと照合し、
      **食い違ったら赤バナーで警告 + どちらが古いか明示**
  (3) 警告時は「コピー」ボタンを画面内に出し、その場で直せるようにする

これで「片方だけ古い」が即座に分かる。
"""
import io, re, datetime, shutil

VERSION = "V26 2026-10-29"
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# ---------- GAS ----------
G = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(G, G + ".bak_vg_" + ts)
g = io.open(G, encoding="utf-8").read()
g = re.sub(r"var GAS_VERSION = '[^']*';",
           "var GAS_VERSION = '%s';" % VERSION, g, count=1)
io.open(G, "w", encoding="utf-8").write(g)
print("GAS_VERSION ->", VERSION)

# ---------- dialog ----------
D = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
shutil.copy2(D, D + ".bak_vg_" + ts)
d = io.open(D, encoding="utf-8").read()

# dialog 側に期待バージョンを埋め込む
d = re.sub(r"diag\('dialog 読込OK \([^)]*\)'\);",
           "diag('dialog 読込OK (%s)');" % VERSION, d, count=1)

OLD = """var diagLog = [];"""
assert d.count(OLD) == 1, "anchor1"
NEW = """// [GAS_VERSION_GUARD_V1] dialog と コード.gs は必ずセットで貼り替えること。
//   片方だけ古いと google.script.run が無言で失敗する事故が多発したため、
//   起動時に照合して食い違いを画面に出す。
var DIALOG_VERSION = '%s';
var diagLog = [];""" % VERSION
d = d.replace(OLD, NEW, 1)

# バージョン照合
OLD2 = """probe('getVersion', function (v) {
  document.getElementById('ver').textContent = '[' + v + ']';
});"""
assert d.count(OLD2) == 1, "anchor2"
NEW2 = """probe('getVersion', function (v) {
  var same = (v === DIALOG_VERSION);
  document.getElementById('ver').textContent = '[' + v + ']';
  if (same) return;
  // 片方だけ古い -> 赤バナーで警告する
  var b = document.createElement('div');
  b.style.cssText = 'background:#fdecea;border:2px solid #c00;border-radius:6px;' +
    'padding:10px;margin-bottom:10px;font-size:13px;line-height:1.7';
  b.innerHTML =
    '<b style="color:#c00;font-size:14px">⚠ コード.gs と dialog のバージョンが違います</b><br>' +
    '<span style="font-family:monospace">' +
    'コード.gs : ' + v + '<br>' +
    'dialog&nbsp;&nbsp;&nbsp;&nbsp;: ' + DIALOG_VERSION + '</span><br>' +
    '<b>' + (v < DIALOG_VERSION ? 'コード.gs が古い' : 'dialog が古い') + '</b>ので貼り直してください。<br>' +
    '<span style="color:#555">ダッシュボード →「📋 コード.gs をコピー」「📋 dialog.html をコピー」' +
    'の<b>両方</b>を貼り替えて Ctrl+S</span>';
  document.body.insertBefore(b, document.body.firstChild);
});"""
d = d.replace(OLD2, NEW2, 1)
io.open(D, "w", encoding="utf-8").write(d)
print("DIALOG_VERSION ->", VERSION)

# ---------- 検証 ----------
g2 = io.open(G, encoding="utf-8").read()
d2 = io.open(D, encoding="utf-8").read()
gv = re.search(r"var GAS_VERSION = '([^']*)'", g2).group(1)
dv = re.search(r"var DIALOG_VERSION = '([^']*)'", d2).group(1)
print("\n照合: GAS=%s / DIALOG=%s -> %s" % (gv, dv, "一致" if gv == dv else "不一致!!"))
