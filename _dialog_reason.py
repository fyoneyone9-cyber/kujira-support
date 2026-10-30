# -*- coding: utf-8 -*-
"""[KOUTEI_REASON_V1] 工程管理ダイアログに判定根拠を表示する。"""
import io, shutil, datetime, re

ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# ========== 工程管理ダイアログ ==========
P = r"C:\GensparkClaw\kujira-support\public\docs\koutei-gas-dialog.html"
shutil.copy2(P, P + ".bak_reason_" + ts)
s = io.open(P, encoding="utf-8").read()

# 根拠の表示欄を各行に追加
OLD = """  var html = CATS.map(function (c, i) {
    return '<div class="chk">' +
      '<input type="checkbox" id="c' + i + '">' +
      '<label for="c' + i + '">' + c.name + '</label>' +
      '<span class="auto" id="a' + i + '"></span></div>';
  }).join('');"""
assert s.count(OLD) == 1, "anchor1"
NEW = """  var html = CATS.map(function (c, i) {
    return '<div class="chk">' +
      '<input type="checkbox" id="c' + i + '">' +
      '<label for="c' + i + '">' + c.name + '</label>' +
      '<span class="auto" id="a' + i + '"></span></div>' +
      '<div class="why" id="w' + i + '"></div>';
  }).join('');"""
s = s.replace(OLD, NEW, 1)

# スタイル
OLD2 = """ .chk .auto{font-size:11px;color:#0b8043}"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """ .chk .auto{font-size:11px;color:#0b8043}
 .why{font-size:11px;color:#888;margin:-2px 0 4px 26px;line-height:1.4}
 .why.on{color:#0b8043}
 .why.off{color:#999}"""
s = s.replace(OLD2, NEW2, 1)

# applyJson で根拠を出す
OLD3 = """  var n = 0;
  CATS.forEach(function (c, i) {
    var v = (c.key === 'always') || !!on[c.key];
    document.getElementById('c' + i).checked = v;
    document.getElementById('a' + i).textContent = v ? '自動' : '';
    if (v) n++;
  });
  document.getElementById('msg').innerHTML =
    '<b style="color:#0b8043">✅ 反映しました</b>（' + n + '区分を自動選択）<br>' +
    '<span style="font-size:12px;color:#888">違う場合はチェックを直してください</span>';"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """  // [KOUTEI_REASON_V1] なぜON/OFFかを各行に表示する
  var why = d.reasons || {};
  var n = 0;
  CATS.forEach(function (c, i) {
    var v = (c.key === 'always') || !!on[c.key];
    document.getElementById('c' + i).checked = v;
    document.getElementById('a' + i).textContent = v ? '自動' : '';
    var w = document.getElementById('w' + i);
    if (w) {
      var txt;
      if (c.key === 'always') txt = '必ず残す工程です';
      else if (!c.key) txt = '区分を判定できないため、残します（手動で確認してください）';
      else if (why[c.key]) txt = why[c.key];
      else txt = v ? '対象あり' : '対象なし';
      w.textContent = (v ? '✅ ' : '－ ') + txt;
      w.className = 'why ' + (v ? 'on' : 'off');
    }
    if (v) n++;
  });
  document.getElementById('msg').innerHTML =
    '<b style="color:#0b8043">✅ 反映しました</b>（' + n + '/' + CATS.length + ' 区分をON）<br>' +
    '<span style="font-size:12px;color:#888">各行の下に判定の理由を出しています。違う場合はチェックを直してください</span>';"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("工程管理ダイアログ: 根拠表示を追加")

# ========== ヒアリングダイアログも同様に ==========
P2 = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
shutil.copy2(P2, P2 + ".bak_reason_" + ts)
h = io.open(P2, encoding="utf-8").read()

OLD4 = """    var on = 0;
    SHEETS.forEach(function (n, i) {
      var v = !!set[n];
      document.getElementById('t' + i).checked = v;
      document.getElementById('a' + i).textContent = v ? '自動' : '';
      if (v) on++;
    });"""
if h.count(OLD4) == 1:
    NEW4 = """    // [KOUTEI_REASON_V1] 判定の根拠を各行に出す
    var why = d.reasons || {};
    var KEYMAP = {
      'PMS': 'pms', 'スマートロック': 'smartlock', 'カードキー': 'cardkey',
      'シリンダー': 'cylinder', '現金': 'cash', '端末カード': 'p400',
      'スマホカード': 'sumaho', 'PayPay': 'paypay', 'プリンタ': 'printer',
      'ルームタブレット': 'roomtablet', '事前チェックイン': 'precheckin', '工事': 'koji'
    };
    var on = 0;
    SHEETS.forEach(function (n, i) {
      var v = !!set[n];
      document.getElementById('t' + i).checked = v;
      document.getElementById('a' + i).textContent = v ? '自動' : '';
      var w = document.getElementById('w' + i);
      if (w) {
        var txt = '';
        if (n.indexOf('必須確認') >= 0 || n.indexOf('表紙') >= 0) txt = '必ず残すシートです';
        else {
          for (var kw in KEYMAP) {
            if (n.indexOf(kw) >= 0 && why[KEYMAP[kw]]) { txt = why[KEYMAP[kw]]; break; }
          }
          if (!txt) txt = v ? '対象あり' : '対象なし';
        }
        w.textContent = (v ? '✅ ' : '－ ') + txt;
        w.className = 'why ' + (v ? 'on' : 'off');
      }
      if (v) on++;
    });"""
    h = h.replace(OLD4, NEW4, 1)

    # 行に why 用の div を追加
    OLD5 = """      '<span class="auto" id="a' + i + '"></span></div>';
  }).join('');"""
    if h.count(OLD5) == 1:
        NEW5 = """      '<span class="auto" id="a' + i + '"></span></div>' +
      '<div class="why" id="w' + i + '"></div>';
  }).join('');"""
        h = h.replace(OLD5, NEW5, 1)

    OLD6 = """ .chk .auto{font-size:11px;color:#0b8043}"""
    if h.count(OLD6) == 1:
        h = h.replace(OLD6, OLD6 + """
 .why{font-size:11px;color:#888;margin:-2px 0 4px 26px;line-height:1.4}
 .why.on{color:#0b8043}
 .why.off{color:#999}""", 1)
    io.open(P2, "w", encoding="utf-8").write(h)
    print("ヒアリングダイアログ: 根拠表示を追加")
else:
    print("ヒアリングダイアログ: アンカー不一致（スキップ）")
