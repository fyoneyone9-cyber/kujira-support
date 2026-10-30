# -*- coding: utf-8 -*-
"""[HEARING_GAS_V8 2026-10-29] 分かっている情報を全シート・全項目に反映する。

これまで必須確認②の6項目だけだった。
調査(_scan_fillable.py)の結果、以下にも入れられる:
  必須確認②  : 組織名/代表メール/代表電話/ログイン者名/物件名/住所/郵便番号/
                領収書電話/緊急連絡先/部屋総数
  カードキー  : メーカー / 担当者名 / 電話 / メール
  PayPay決済  : 担当者名 / メールアドレス
  必須確認③  : 部屋情報（客室数）
  PMS         : PMS名
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
bak = P + ".bak_fillall_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

i = s.index("/** 必須確認②に案件情報を書き込む")
NEW = '''/**
 * 分かっている情報を全シートに書き込む。
 * 「項目名を含む行」を探し、その行の回答欄に値を入れる。
 * 既に値がある場合は上書きしない。
 */
function fillInfo(ss, p) {
  var zip = '', addr = p.property || '';
  var m = addr.match(/〒?\\s*(\\d{3}-?\\d{4})/);
  if (m) { zip = m[1]; addr = addr.replace(m[0], '').trim(); }

  // シート名 -> [[項目名に含まれる語, 入れる値], ...]
  // 上にあるものから順に照合し、最初に当たったものを使う。
  var PLAN = {
    '必須確認②': [
      ['組織名',                         p.client],
      ['メールアドレス（代表）',           p.email],
      ['お電話番号（代表）',              p.tel],
      ['DMSにログインされる方のお名前',    p.contact],
      ['DMSにログインされる方のメールアドレス', p.email],
      ['物件名',                         p.propertyName || addr],
      ['物件の住所',                      addr],
      ['物件の郵便番号',                  zip],
      ['領収書に印字する電話番号',         p.tel],
      ['緊急連絡先電話番号',              p.tel],
      ['物件内にあるお部屋の総数',         p.rooms]
    ],
    '必須確認③': [
      ['お部屋の総数', p.rooms]
    ],
    'PMS': [
      ['PMSの名称', p.pms],
      ['ご利用のPMS', p.pms]
    ],
    'カードキー': [
      ['メーカーをご回答',  p.cardkeyMaker],
      ['お名前',           p.contact],
      ['携帯電話番号',      p.tel],
      ['メールアドレス',    p.email]
    ],
    'PayPay決済': [
      ['お名前',        p.contact],
      ['メールアドレス', p.email]
    ],
    'スマートロック①': [
      ['メーカー', p.lockMaker]
    ]
  };

  var filled = 0;
  for (var sheetName in PLAN) {
    var sh = ss.getSheetByName(sheetName);
    if (!sh) continue;
    var last = sh.getLastRow(), lastCol = sh.getLastColumn();
    if (last < 1 || lastCol < 1) continue;
    var values = sh.getRange(1, 1, last, lastCol).getValues();

    // 『ご回答欄』の列を探す（シートごとに違う）
    var ansCol = 0;
    for (var r = 0; r < Math.min(6, values.length); r++) {
      for (var c = 0; c < values[r].length; c++) {
        if (String(values[r][c]).indexOf('ご回答欄') >= 0) { ansCol = c + 1; break; }
      }
      if (ansCol) break;
    }
    if (!ansCol) continue;

    var plan = PLAN[sheetName];
    var usedRow = {};
    for (var pi = 0; pi < plan.length; pi++) {
      var key = plan[pi][0], val = plan[pi][1];
      if (!val) continue;
      for (var r2 = 0; r2 < values.length; r2++) {
        if (usedRow[r2]) continue;
        if (values[r2].join(' ').indexOf(key) < 0) continue;
        var cell = sh.getRange(r2 + 1, ansCol);
        if (!cell.getValue()) { cell.setValue(val); filled++; }
        usedRow[r2] = true;
        break;
      }
    }
  }
  return filled;
}

/** 旧版の名前での呼び出しにも対応 */
'''
s = s[:i] + NEW
io.open(P, "w", encoding="utf-8").write(s)
print("rewritten fillInfo")
