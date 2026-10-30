# -*- coding: utf-8 -*-
"""[PAYPAY_APPLY_V2 2026-10-29] CCをユーザー指定の3件に絞る。
元テンプレには導入支援メンバー全員が並んでいたが、実運用では不要とのこと。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_cc_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                            const CC = ['mao.hisaoka@paypay-corp.co.jp', 'shohei_noda@device-agency.co.jp',
                              'humitaka_yoneyama@device-agency.co.jp', 'yoshie_kikuti@device-agency.co.jp',
                              'tadashi_hashimoto@kujira.co.jp', 'izuoka@kujira.co.jp'].join(',')"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)
NEW = """                            // [PAYPAY_APPLY_V2 2026-10-29] CCはこの3件のみ（ユーザー指定）
                            const CC = ['mao.hisaoka@paypay-corp.co.jp',
                              'tadashi_hashimoto@kujira.co.jp',
                              'support@and-iot.jp'].join(',')"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
