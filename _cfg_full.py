# -*- coding: utf-8 -*-
"""[HEARING_GAS_V8] 「設定をコピー」で渡す情報を全部入りにする。
会社名/住所/担当者/電話に加えて、メール・物件名・部屋数・PMS名・
カードキーメーカー・スマートロックメーカーも渡す。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_cfgfull_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                      const cfg = {
                                        client: it.client_name || '',
                                        property: it.install_address || '',
                                        contact: it.contact_name || '',
                                        tel: it.contact_tel1 || it.contact_tel2 || '',
                                        equips,
                                      }"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                      // [HEARING_GAS_V8 2026-10-29] 分かっている情報は全部渡す。
                                      //   equipItems から機材名・メーカー・台数も拾う。
                                      const pick = (re: RegExp) => {
                                        const e = equipItems.find(x => re.test((x.name || '') + ' ' + (x.value || '')))
                                        return e ? String(e.value || e.name || '').trim() : ''
                                      }
                                      const roomsRaw = equipItems
                                        .map(e => String(e.value || '').match(/(\\d+)\\s*室/))
                                        .find(Boolean)
                                      const cfg = {
                                        client: it.client_name || '',
                                        property: it.install_address || '',
                                        propertyName: it.property_name || '',
                                        contact: it.contact_name || '',
                                        tel: it.contact_tel1 || it.contact_tel2 || '',
                                        email: it.contact_email || '',
                                        rooms: roomsRaw ? roomsRaw[1] : '',
                                        pms: pick(/PMS/i),
                                        cardkeyMaker: pick(/カードキー|MIWA|GOAL|LEGEND|ASSA/i),
                                        lockMaker: pick(/スマートロック|EPIC|TTLock|KEYVOX|Baycom|SwitchBot/i),
                                        equips,
                                      }"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
