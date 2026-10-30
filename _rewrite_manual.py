# -*- coding: utf-8 -*-
"""[HEARING_MANUAL_V1 2026-10-29] 手順を「毎回やること」中心に書き直す。

指摘:「📋設定をコピーがマニュアルにない、わかりづらい」
  設置手順(初回)の中に毎回の操作が埋もれていて、
  普段使う「設定をコピー→貼り付け」が目立たなかった。

構成を変える:
  ・常時表示 = 毎回の3ステップ（これが本体）
  ・折りたたみ = 初回だけの設置手順
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_manual_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# ボタン行の直後に「毎回の手順」を常時表示で入れる
ANCHOR = """                                  <a href="/docs/hearing-gas-dialog.html" target="_blank" rel="noreferrer"
                                    className="text-sm px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
                                    title="Apps Scriptに貼り付けるHTML（初回のみ）">
                                    📜 dialog.html
                                  </a>
                                </div>"""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = """                                  <a href="/docs/hearing-gas-dialog.html" target="_blank" rel="noreferrer"
                                    className="text-sm px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
                                    title="Apps Scriptに貼り付けるHTML（初回のみ）">
                                    📜 dialog.html
                                  </a>
                                </div>

                                {/* [HEARING_MANUAL_V1 2026-10-29] 毎回やる操作を常時表示する。
                                    初回の設置手順に埋もれて「設定をコピー」が見つけにくかった。 */}
                                <div className="mt-2 bg-slate-900/60 border border-slate-700 rounded-lg p-2.5">
                                  <p className="text-sm font-bold text-amber-300 mb-1.5">▶ 作成手順（毎回これだけ）</p>
                                  <div className="space-y-1.5 text-sm text-slate-300 leading-relaxed">
                                    <div className="flex gap-2 items-start">
                                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">1</span>
                                      <span>
                                        上の <b className="text-amber-300">📋 設定をコピー</b> を押す
                                        <br />
                                        <span className="text-slate-500">会社名・住所・担当者・電話・メール・機材構成がまとめてコピーされます</span>
                                      </span>
                                    </div>
                                    <div className="flex gap-2 items-start">
                                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">2</span>
                                      <span>
                                        自分のシートを開き、メニュー
                                        <b className="text-amber-300"> 📋 ヒアリングシート → 必要シートだけコピー作成</b>
                                      </span>
                                    </div>
                                    <div className="flex gap-2 items-start">
                                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">3</span>
                                      <span>
                                        一番上の欄に <b>貼り付け</b> →
                                        <b className="text-amber-300"> ⬇ 貼り付けた内容を反映</b> →
                                        <b className="text-emerald-300"> コピーを作成</b>
                                        <br />
                                        <span className="text-slate-500">
                                          機材チェックが自動で入り、17箇所に案件情報が入力されます
                                        </span>
                                      </span>
                                    </div>
                                  </div>
                                </div>"""
s = s.replace(ANCHOR, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
