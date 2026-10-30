# -*- coding: utf-8 -*-
"""[HEARING_GAS_V8] ダイアログに追加項目(メール/部屋数/PMS/メーカー)を出す。
貼り付けで自動反映され、手修正もできるようにする。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
bak = P + ".bak_full_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """<label>電話番号</label>
<input type="text" id="tel" placeholder="0799-00-0000">"""
assert s.count(OLD) == 1, "anchor1"
NEW = """<label>電話番号</label>
<input type="text" id="tel" placeholder="0799-00-0000">
<label>メールアドレス</label>
<input type="text" id="email" placeholder="info@example.com">
<label>客室数</label>
<input type="text" id="rooms" placeholder="20">
<label>PMS名</label>
<input type="text" id="pms" placeholder="suitebook">
<label>カードキーのメーカー</label>
<input type="text" id="cardkeyMaker" placeholder="MIWA">
<label>スマートロックのメーカー</label>
<input type="text" id="lockMaker" placeholder="EPIC">"""
s = s.replace(OLD, NEW, 1)

OLD2 = """  if(d.client)   document.getElementById('client').value = d.client;
  if(d.property) document.getElementById('property').value = d.property;
  if(d.contact)  document.getElementById('contact').value = d.contact;
  if(d.tel)      document.getElementById('tel').value = d.tel;"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """  ['client','property','contact','tel','email','rooms','pms','cardkeyMaker','lockMaker']
    .forEach(function(k){ if(d[k]) document.getElementById(k).value = d[k]; });"""
s = s.replace(OLD2, NEW2, 1)

OLD3 = """    .createCopy({
      client:   document.getElementById('client').value,
      property: document.getElementById('property').value,
      contact:  document.getElementById('contact').value,
      tel:      document.getElementById('tel').value,
      equips:   equips
    });"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """    .createCopy({
      client:       document.getElementById('client').value,
      property:     document.getElementById('property').value,
      contact:      document.getElementById('contact').value,
      tel:          document.getElementById('tel').value,
      email:        document.getElementById('email').value,
      rooms:        document.getElementById('rooms').value,
      pms:          document.getElementById('pms').value,
      cardkeyMaker: document.getElementById('cardkeyMaker').value,
      lockMaker:    document.getElementById('lockMaker').value,
      equips:       equips
    });"""
s = s.replace(OLD3, NEW3, 1)

# 完了メッセージに自動入力件数を出す
OLD4 = """    '削除したシート: ' + r.removed.length + '枚<br>' +"""
assert s.count(OLD4) == 1, "anchor4"
NEW4 = """    '削除したシート: ' + r.removed.length + '枚<br>' +
    '自動入力: ' + (r.filled || 0) + '箇所<br>' +"""
s = s.replace(OLD4, NEW4, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
