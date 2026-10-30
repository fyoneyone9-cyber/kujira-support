# -*- coding: utf-8 -*-
"""[HEARING_GAS_V20 2026-10-29] 施設名と住所を分けて自動入力する。

これまで「物件名」に住所を入れていたが、申込書から施設名
（例: ビジョングランピング淡路）が取れるようになったので分離する。

  物件名      -> 施設名
  物件の住所  -> 設置先住所
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js"
shutil.copy2(P, P + ".bak_v20_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """function fillInfo(ss, p) {
  var zip = '', addr = p.property || '';
  var m = addr.match(/〒?\\s*(\\d{3}-?\\d{4})/);
  if (m) { zip = m[1]; addr = addr.replace(m[0], '').trim(); }"""
assert s.count(OLD) == 1, "anchor1"
NEW = """function fillInfo(ss, p) {
  // [V20] 施設名と住所は別物。申込書から施設名が取れるので分けて使う。
  //   p.property = 施設名（例: ビジョングランピング淡路）
  //   p.address  = 設置先住所。無ければ property を住所として扱う。
  var addr = p.address || p.property || '';
  var zip = '';
  var m = addr.match(/〒?\\s*(\\d{3}-?\\d{4})/);
  if (m) { zip = m[1]; addr = addr.replace(m[0], '').trim(); }
  var facility = p.property || addr;"""
s = s.replace(OLD, NEW, 1)

OLD2 = """      ['物件名',                         p.propertyName || addr],"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """      ['物件名',                         facility],"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
