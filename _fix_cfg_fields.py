# -*- coding: utf-8 -*-
"""[HEARING_GAS_V8b] 存在しないフィールドを実在するものに置き換える。

tscで判明: DeliveryItem に property_name / contact_email は無い。
  物件名  -> 無いので住所で代用（propertyName は送らない）
  メール  -> worker_contacts[].email を使う
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_cfgfix_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                        propertyName: it.property_name || '',
                                        contact: it.contact_name || '',
                                        tel: it.contact_tel1 || it.contact_tel2 || '',
                                        email: it.contact_email || '',"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)
NEW = """                                        contact: it.contact_name || '',
                                        tel: it.contact_tel1 || it.contact_tel2 || '',
                                        // メールは専用列が無いので作業員連絡先から拾う
                                        email: (it.worker_contacts || []).map(w => w?.email).find(Boolean) || '',"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
