# -*- coding: utf-8 -*-
"""[HEARING_GAS_V20b] ダイアログに「設置先住所」を追加し、施設名と分ける。"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas-dialog.html"
shutil.copy2(P, P + ".bak_addr_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """<label>物件名・住所</label>
<input type="text" id="property" placeholder="〒656-2401 兵庫県淡路市岩屋2604">"""
assert s.count(OLD) == 1, "anchor1"
NEW = """<label>施設名（物件名）</label>
<input type="text" id="property" placeholder="ビジョングランピング淡路">
<label>設置先住所</label>
<input type="text" id="address" placeholder="〒656-2401 兵庫県淡路市岩屋2604">"""
s = s.replace(OLD, NEW, 1)

OLD2 = """  ['client', 'property', 'contact', 'tel', 'email', 'rooms']"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """  ['client', 'property', 'address', 'contact', 'tel', 'email', 'rooms']"""
s = s.replace(OLD2, NEW2, 1)

OLD3 = """      property: document.getElementById('property').value,"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """      property: document.getElementById('property').value,
      address:  document.getElementById('address').value,"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
