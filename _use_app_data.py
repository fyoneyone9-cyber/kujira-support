# -*- coding: utf-8 -*-
"""[APPLICATION_USE_V1 2026-10-29] 申込書の情報を各機能で活用する。

強化する箇所:
  (1) ヒアリングシートの「設定をコピー」
      施設名 → 物件名（これまで住所で代用していた）
      客室数 → 部屋の総数
      担当者/電話/メール → 申込書の値を優先
  (2) PayPay利用申請メール
      屋号名に施設名を使う（住所の流用をやめる）
  (3) 事前準備お願いメール
      宛名に担当者名を使う
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_useapp_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

# (1) 設定コピー: 申込書の値を優先する
OLD = """                                      const cfg = {
                                        client: it.client_name || '',
                                        property: it.install_address || '',
                                        contact: it.contact_name || '',"""
assert s.count(OLD) == 1, "anchor1: %d" % s.count(OLD)
NEW = """                                      // [APPLICATION_USE_V1] 申込書を取り込んでいればそちらを優先する。
                                      //   施設名は申込書にしか無い情報なので特に重要。
                                      const td2 = it.dashboard_todos || {}
                                      const appStr = (k: string) => (td2[k] as string) || ''
                                      const cfg = {
                                        client: it.client_name || '',
                                        property: appStr('app_facility') || it.install_address || '',
                                        address: appStr('app_site_addr') || it.install_address || '',
                                        contact: appStr('app_contact') || it.contact_name || '',"""
s = s.replace(OLD, NEW, 1)

OLD2 = """                                        tel: it.contact_tel1 || it.contact_tel2 || '',
                                        // [CLIENT_EMAIL_V1] 手入力したお客様メール優先、無ければ作業員連絡先
                                        email: (it.dashboard_todos?.['client_email'] as string)
                                          || (it.worker_contacts || []).map(w => w?.email).find(Boolean) || '',
                                        rooms: roomsRaw ? roomsRaw[1] : '',"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """                                        tel: appStr('app_tel') || it.contact_tel1 || it.contact_tel2 || '',
                                        // 手入力したお客様メール > 申込書 > 作業員連絡先
                                        email: appStr('client_email') || appStr('app_email')
                                          || (it.worker_contacts || []).map(w => w?.email).find(Boolean) || '',
                                        rooms: appStr('app_rooms') || (roomsRaw ? roomsRaw[1] : ''),"""
s = s.replace(OLD2, NEW2, 1)

# (2) PayPay申請メール: 屋号名に施設名
OLD3 = """屋号名　${it.install_address ? it.install_address.replace(/^〒?[0-9\\-]+\\s*/, '') : '●●●'}"""
if s.count(OLD3) == 1:
    NEW3 = """屋号名　${(it.dashboard_todos?.['app_facility'] as string) || (it.install_address ? it.install_address.replace(/^〒?[0-9\\-]+\\s*/, '') : '●●●')}"""
    s = s.replace(OLD3, NEW3, 1)
    print("  PayPay申請メール: 屋号名に施設名を使用")

# (3) PayPay申請メールの担当者・電話も申込書優先
OLD4 = """                            const tel = it.contact_tel1 || it.contact_tel2 || ''"""
if s.count(OLD4) == 1:
    NEW4 = """                            const tel = (it.dashboard_todos?.['app_tel'] as string)
                              || it.contact_tel1 || it.contact_tel2 || ''"""
    s = s.replace(OLD4, NEW4, 1)
    print("  PayPay申請メール: 電話を申込書優先")

OLD5 = """ご担当者　${it.contact_name || '●●'} 様"""
if s.count(OLD5) == 1:
    NEW5 = """ご担当者　${(it.dashboard_todos?.['app_contact'] as string) || it.contact_name || '●●'} 様"""
    s = s.replace(OLD5, NEW5, 1)
    print("  PayPay申請メール: 担当者を申込書優先")

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
