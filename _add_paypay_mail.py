# -*- coding: utf-8 -*-
"""[PAYPAY_APPLY_V1 2026-10-29] PayPay利用申請テンプレートをPayPay欄の近くに追加する。

要望:「PayPayの近くに入れといて、使用申請テンプレート。自動で埋めれる所はコマ毎に埋めて」

自動差し込み:
  法人名      -> client_name
  屋号名      -> install_address から施設名を推定（なければ空欄のまま）
  URL        -> dashboard_todos.hotel_url があれば
  ご担当者    -> contact_name
  物件電話番号 -> contact_tel1
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_ppmail_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# PayCube未発注ブロックの直後(= 機材ステータス欄の中)に差し込む
ANCHOR = """                          {/* PayCube未発注時: 発注書雛形・社長承認リンク */}"""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = """                          {/* [PAYPAY_APPLY_V1 2026-10-29] PayPay利用申請メール（自動差し込み） */}
                          {name === 'PayPay' && (() => {
                            const PP_SUBJECT = `PayPayAPI接続対象店舗追加のご依頼（スマートチェックインシステム）：${it.client_name || '●●●'}`
                            const tel = it.contact_tel1 || it.contact_tel2 || ''
                            const url = (it.dashboard_todos?.['hotel_url'] as string) || ''
                            const PP_BODY = `PayPay株式会社 天明様

いつもお世話になっております。
株式会社デバイスエージェンシーの●●です。

以下の弊社クライアント様が新規にPayPayを利用されたいとのことで、たびたびお手数おかけしますが、API接続のお手続きをお願いします。

法人名or個人事業主名　${it.client_name || '●●●'}

屋号名　${it.install_address ? it.install_address.replace(/^〒?[0-9\\-]+\\s*/, '') : '●●●'}

下記のいずれか
 ・店舗の外観写真と内観写真
 ・店舗の所在がわかるwebサイトのURL
 ・営業許可書またはチラシ(オープン前で写真の入手が難しい場合)

URL記入　${url || '(例：https://www.device-agency.com)'}

ご担当者　${it.contact_name || '●●'} 様
メールアドレス　(例test@device-agency.co.jp)

物件電話番号　${tel || '(例：024-000-0000)'}

個人電話番号（分かれば）　(例：090-0000-0000)

システムフロー
システムマニュアル
https://drive.google.com/file/d/1RlAcIFJH9jDioix30SPCgsE6FTmBgW3z/view
※P42の精算方法選択画面が該当します。ただしPayPayは一部のユーザー様への機能開示であることから、汎用マニュアルであるこのマニュアルの画面イメージには搭載しておりません

画面遷移図
https://drive.google.com/file/d/1D7rtpNwEgKuuOnB1-mjEirG-MPjsxAP9/view

お忙しい中恐れ入りますが、よろしくお願いします。`
                            const TO = 'kenta.temmyo@paypay-corp.co.jp'
                            const CC = ['mao.hisaoka@paypay-corp.co.jp', 'shohei_noda@device-agency.co.jp',
                              'humitaka_yoneyama@device-agency.co.jp', 'yoshie_kikuti@device-agency.co.jp',
                              'tadashi_hashimoto@kujira.co.jp', 'izuoka@kujira.co.jp'].join(',')
                            return (
                              <div className="mt-1.5 bg-rose-950/30 border border-rose-800/50 rounded px-2 py-1.5 space-y-1">
                                <div className="flex items-center gap-1.5 flex-wrap">
                                  <span className="text-[11px] text-rose-300 font-bold">📨 PayPay利用申請:</span>
                                  <button onClick={() => {
                                    navigator.clipboard.writeText(PP_SUBJECT)
                                      .then(() => alert('✅ 件名をコピーしました')).catch(() => alert('コピー失敗'))
                                  }} className="text-[11px] px-2 py-0.5 rounded bg-slate-700 hover:bg-blue-700 text-slate-200">
                                    📋 件名
                                  </button>
                                  <button onClick={() => {
                                    navigator.clipboard.writeText(PP_BODY)
                                      .then(() => alert('✅ 本文をコピーしました（案件情報を差し込み済み）')).catch(() => alert('コピー失敗'))
                                  }} className="text-[11px] px-2 py-0.5 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                    📋 本文
                                  </button>
                                  <a href={`mailto:${TO}?cc=${encodeURIComponent(CC)}&subject=${encodeURIComponent(PP_SUBJECT)}&body=${encodeURIComponent(PP_BODY)}`}
                                    className="text-[11px] px-2 py-0.5 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
                                    ✉️ メール作成（TO/CC入り）
                                  </a>
                                </div>
                                <p className="text-[11px] text-rose-200/60">
                                  差し込み済: 法人名 / 屋号名 / ご担当者 / 物件電話番号　※「●●」の箇所は手入力してください
                                </p>
                              </div>
                            )
                          })()}
                          {/* PayCube未発注時: 発注書雛形・社長承認リンク */}"""
s = s.replace(ANCHOR, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
