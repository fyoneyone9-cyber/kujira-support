# -*- coding: utf-8 -*-
"""[HEARING_AUTOFILL_V1] UI側から fill（自動入力データ）を送る。"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_fillui_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                        prefill: {
                                          'スマートロック': hasLock2 ? 'TRUE' : 'FALSE',
                                          'カードキー': hasCard ? 'TRUE' : 'FALSE',
                                          'シリンダー錠': hasCyli ? 'TRUE' : 'FALSE',
                                          'PMS': hasPms2 ? 'TRUE' : 'FALSE',
                                          'プリンタ': hasPrinter ? 'TRUE' : 'FALSE',
                                          'ルームタブレット': hasTablet ? 'TRUE' : 'FALSE',
                                        },"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                        prefill: {
                                          'スマートロック': hasLock2 ? 'TRUE' : 'FALSE',
                                          'カードキー': hasCard ? 'TRUE' : 'FALSE',
                                          'シリンダー錠': hasCyli ? 'TRUE' : 'FALSE',
                                          'PMS': hasPms2 ? 'TRUE' : 'FALSE',
                                          'プリンタ': hasPrinter ? 'TRUE' : 'FALSE',
                                          'ルームタブレット': hasTablet ? 'TRUE' : 'FALSE',
                                        },
                                        // [HEARING_AUTOFILL_V1 2026-10-29] 案件情報を回答欄へ自動入力。
                                        //   項目名で行を探して書くので行番号は決め打ちしない。
                                        fill: (() => {
                                          const addr = it.install_address || ''
                                          const zip = (addr.match(/〒?\\s*(\\d{3}-?\\d{4})/) || [])[1] || ''
                                          const addrNoZip = addr.replace(/〒?\\s*\\d{3}-?\\d{4}\\s*/, '').trim()
                                          const tel = it.contact_tel1 || it.contact_tel2 || ''
                                          const o: Record<string, string> = {}
                                          if (it.client_name) {
                                            o['組織名'] = it.client_name
                                            o['法人名'] = it.client_name
                                          }
                                          if (it.contact_name) {
                                            o['DMSにログインされる方のお名前'] = it.contact_name
                                            o['ご担当者様のお名前'] = it.contact_name
                                          }
                                          if (addrNoZip) {
                                            o['物件名'] = addrNoZip
                                            o['物件の住所'] = addrNoZip
                                          }
                                          if (zip) o['物件の郵便番号'] = zip
                                          if (tel) {
                                            o['お電話番号'] = tel
                                            o['領収書に印字する電話番号'] = tel
                                          }
                                          return o
                                        })(),"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
