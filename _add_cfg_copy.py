# -*- coding: utf-8 -*-
"""[HEARING_GAS_V7 2026-10-29] 機材チェックを自動化する。

指摘:「自動で必要なのにチェックついてないじゃん」
  Apps Script側は独立して動くので、ダッシュボードの判定結果を知らなかった。

対策: ダッシュボードに「📋 設定をコピー」ボタンを置き、
      案件情報＋機材フラグをJSONでコピー → ダイアログに貼ると自動でチェックが入る。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_cfgcopy_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

ANCHOR = """                                  <a href="/docs/hearing-gas.js" target="_blank" rel="noreferrer\""""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = """                                  {/* [HEARING_GAS_V7 2026-10-29] 機材判定の結果をJSONでコピーし、
                                      Apps Scriptのダイアログに貼ると自動でチェックが入る。 */}
                                  <button
                                    onClick={() => {
                                      const equips: string[] = []
                                      if (hasPms2) equips.push('pms')
                                      if (hasLock2) equips.push('smartlock')
                                      if (hasCard) equips.push('cardkey')
                                      if (hasCyli) equips.push('cylinder')
                                      if (hasPaycube) equips.push('cash')
                                      if (hasP400) equips.push('p400')
                                      if (hasSumaho) equips.push('sumaho')
                                      if (hasPaypay) equips.push('paypay')
                                      if (hasPrinter) equips.push('printer')
                                      if (hasTablet) equips.push('roomtablet')
                                      equips.push('precheckin')
                                      const cfg = {
                                        client: it.client_name || '',
                                        property: it.install_address || '',
                                        contact: it.contact_name || '',
                                        tel: it.contact_tel1 || it.contact_tel2 || '',
                                        equips,
                                      }
                                      navigator.clipboard.writeText(JSON.stringify(cfg))
                                        .then(() => alert('✅ 設定をコピーしました（機材' + (equips.length - 1) + '件）\\n\\nスプレッドシートの「📋 ヒアリングシート」→「必要シートだけコピー作成」を開き、\\n一番上の欄に貼り付けて「⬇ 貼り付けた内容を反映」を押してください'))
                                        .catch(() => alert('コピー失敗'))
                                    }}
                                    className="text-sm px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold transition-colors"
                                    title="この案件の情報と機材チェックをまとめてコピーします">
                                    📋 設定をコピー
                                  </button>
                                  <a href="/docs/hearing-gas.js" target="_blank" rel="noreferrer\""""
s = s.replace(ANCHOR, NEW, 1)

# 使い方の説明にも1ステップ追加
OLD2 = """                                              <p>
                                                ① コピーしたシートのメニュー
                                                <b className="text-amber-300"> 📋 ヒアリングシート</b>（ヘルプの右隣）をクリック
                                              </p>"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """                                              <p className="text-amber-200">
                                                ⓪ 上の <b>📋 設定をコピー</b> を押す（会社名と機材チェックが入ります）
                                              </p>
                                              <p>
                                                ① コピーしたシートのメニュー
                                                <b className="text-amber-300"> 📋 ヒアリングシート</b>（ヘルプの右隣）をクリック
                                              </p>"""
s = s.replace(OLD2, NEW2, 1)

OLD3 = """                                              <p>③ 会社名・物件名・担当者・電話を入力し、導入機材にチェック</p>"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """                                              <p>
                                                ③ 一番上の欄に<b className="text-amber-300">⓪でコピーした内容を貼り付け</b> →
                                                <b> ⬇ 貼り付けた内容を反映</b> を押す<br />
                                                <span className="text-slate-500">会社名・住所・担当者・電話と、機材チェックが自動で入ります</span>
                                              </p>"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
