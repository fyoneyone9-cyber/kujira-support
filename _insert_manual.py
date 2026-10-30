# -*- coding: utf-8 -*-
"""[HEARING_MANUAL_V1 2026-10-29] 毎回の操作を常時表示する（行番号指定で挿入）。"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_manual2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
L = io.open(P, encoding="utf-8").read().split("\n")

# L1765 = "</div>" （ボタン行の閉じ）、L1766 = 設置手順コメント
assert L[1764].strip() == "</div>", "L1765 mismatch: %r" % L[1764]
assert "HEARING_GAS_V2" in L[1765], "L1766 mismatch: %r" % L[1765][:60]

BLOCK = """
                                {/* [HEARING_MANUAL_V1 2026-10-29] 毎回やる操作を常時表示する。
                                    初回の設置手順に埋もれて「設定をコピー」が見つけにくかった。 */}
                                <div className="mt-2 bg-slate-900/60 border border-amber-800/50 rounded-lg p-2.5">
                                  <p className="text-sm font-bold text-amber-300 mb-1.5">▶ 作成手順（毎回これだけ）</p>
                                  <div className="space-y-1.5 text-sm text-slate-300 leading-relaxed">
                                    <div className="flex gap-2 items-start">
                                      <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">1</span>
                                      <span>
                                        上の <b className="text-amber-300">📋 設定をコピー</b> を押す<br />
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
                                        <b className="text-emerald-300"> コピーを作成</b><br />
                                        <span className="text-slate-500">機材チェックが自動で入り、17箇所に案件情報が入力されます</span>
                                      </span>
                                    </div>
                                  </div>
                                </div>
"""
L.insert(1765, BLOCK.rstrip("\n"))
io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("inserted at L1766")
