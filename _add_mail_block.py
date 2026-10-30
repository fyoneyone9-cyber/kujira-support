# -*- coding: utf-8 -*-
"""[HEARING_MAIL_V1 2026-10-29] ヒアリングシート欄に送付メールと添付資料を追加する。

要望: 事前準備のお願いメールと、設置準備PDFをヒアリングシート付近に置きたい。

内容:
  ・件名/本文をワンクリックでコピー（会社名を自動で差し込む）
  ・設置準備PDFを開く（public/docs/setup-guide.pdf）
  ・最新マニュアルURL
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_mail_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

ANCHOR = """                              <span className="text-[11px] text-slate-500">
                                ※ Excelをドライブにドラッグ → 右クリック「Googleスプレッドシートで開く」
                              </span>"""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = ANCHOR + """
                              {/* [HEARING_MAIL_V1 2026-10-29] 送付メール文面と添付資料 */}
                              {(() => {
                                const MAIL_SUBJECT = '【スマートチェックインシステム】機器設置に向けた事前準備のお願い'
                                const MAIL_BODY = `${it.client_name || ''} ご担当者様

いつも大変お世話になっております。
株式会社デバイスエージェンシー 導入支援担当窓口でございます。

この度はスマートチェックインシステムをお申込みいただき、誠にありがとうございます。
機器の設置および設定作業を円滑に進めるため、事前にご確認・ご準備いただきたい事項をご案内申し上げます。

つきましては、下記項目についてご確認およびご手配をお願いできますでしょうか。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
■ チェックイン機設置に伴う事前確認・ご準備事項
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

① ネットワーク環境（Wi-Fi）の確認
チェックイン機本体はWi-Fi接続にて運用いたします。
設置予定場所にて安定してWi-Fi通信が行える環境のご準備をお願いいたします。

② LAN配線のご準備
付属のカード決済端末は有線LAN接続となります。
設置予定位置までLAN配線（規格：Cat5e以上）のお引き回しをお願いいたします。

③ 電源（100V）のご準備
チェックイン機本体から3m以内の壁面コンセント、または「本体設置位置までの距離 ＋ 1m」以上の長さの電源をご用意ください。

④ ネットワーク設定（IPアドレス）の確認
チェックイン機のネットワーク設定にあたり、貴社のネットワーク仕様をお知らせください。
・設定方式：[ DHCP（自動取得） / 固定IP ]
※固定IPをご利用の場合は、割り当て予定のIPアドレス等の情報をご共有いただけますと幸いです。

⑤ ヒアリングシートのご入力 ★【ご返信のお願い】
システム設定に必要な各種情報を把握するため、ヒアリングシートへのご入力をお願いしております。
※本メールに添付しておりますので、ご確認・ご入力のうえご返信をお願いいたします。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

あわせて、設置準備の要点をまとめた資料（PDF）も添付しておりますのでご確認ください。
また、スマートチェックインシステムの最新マニュアルは下記リンクよりいつでもご確認いただけます。
ヒアリングシートご入力の際にもあわせてご参照ください。

▼ 最新マニュアルURL
https://x.gd/9H5wK

ご不明な点やご相談がございましたら、本メールへの返信にてお気軽にお問い合わせください。
引き続き何卒よろしくお願い申し上げます。

株式会社デバイスエージェンシー
導入支援担当窓口`
                                return (
                                  <div className="w-full mt-2 pt-2 border-t border-slate-700/50">
                                    <div className="flex items-center gap-1.5 flex-wrap">
                                      <span className="text-[11px] text-slate-400 font-bold">✉️ 送付メール:</span>
                                      <button
                                        onClick={() => {
                                          navigator.clipboard.writeText(MAIL_SUBJECT)
                                            .then(() => alert('✅ 件名をコピーしました'))
                                            .catch(() => alert('コピー失敗'))
                                        }}
                                        className="text-[11px] px-2 py-1 rounded bg-slate-700 hover:bg-blue-700 text-slate-200 transition-colors">
                                        📋 件名をコピー
                                      </button>
                                      <button
                                        onClick={() => {
                                          navigator.clipboard.writeText(MAIL_BODY)
                                            .then(() => alert('✅ 本文をコピーしました（会社名を差し込み済み）'))
                                            .catch(() => alert('コピー失敗'))
                                        }}
                                        className="text-[11px] px-2 py-1 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold transition-colors">
                                        📋 本文をコピー
                                      </button>
                                      <a href={`mailto:?subject=${encodeURIComponent(MAIL_SUBJECT)}&body=${encodeURIComponent(MAIL_BODY)}`}
                                        className="text-[11px] px-2 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold transition-colors">
                                        ✉️ メール作成
                                      </a>
                                      <a href="/docs/setup-guide.pdf" target="_blank" rel="noreferrer"
                                        className="text-[11px] px-2 py-1 rounded bg-red-800 hover:bg-red-700 text-white font-bold transition-colors"
                                        title="設置準備のご案内（添付用PDF）">
                                        📎 設置準備PDF
                                      </a>
                                      <a href="https://x.gd/9H5wK" target="_blank" rel="noreferrer"
                                        className="text-[11px] px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors">
                                        📘 最新マニュアル
                                      </a>
                                    </div>
                                    <p className="text-[11px] text-slate-500 mt-1">
                                      ※ 添付するもの: ①上の「📥 Excelで作成」のヒアリングシート ②「📎 設置準備PDF」
                                    </p>
                                  </div>
                                )
                              })()}"""
s = s.replace(ANCHOR, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
