# -*- coding: utf-8 -*-
"""[HEARING_GAS_V3 2026-10-29] 設置手順を実情に合わせて書き直す。

判明: 雛形は「（ひな形・閲覧用）」で編集権限が無く、Apps Scriptを設置できない。
      → 先に『ファイル → コピーを作成』で自分のドライブに複製し、
        そのコピーにスクリプトを入れる必要がある。

V2の手順はこの最重要ステップが抜けていた。
あわせて「＋はどこか」「ファイル名に .html は不要」も明記する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_gasv3_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

i = s.index("                                          <div className=\"space-y-1.5 text-[11px] text-slate-300 leading-relaxed\">")
j = s.index("                                          <div className=\"pt-2 border-t border-slate-700\">")

NEW = """                                          <div className="bg-amber-950/40 border border-amber-700/60 rounded px-2 py-1.5 mb-2">
                                            <p className="text-[11px] text-amber-200 font-bold">
                                              ⚠ 雛形は「閲覧用」で編集できません。<br />
                                              まず自分のドライブにコピーを作り、そのコピーに設置します。
                                            </p>
                                          </div>

                                          <div className="space-y-1.5 text-[11px] text-slate-300 leading-relaxed">
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-[10px]">1</span>
                                              <span>上の <b className="text-emerald-300">📄 雛形を開く</b> をクリック</span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-[10px]">2</span>
                                              <span>
                                                <b className="text-amber-300">ファイル → コピーを作成</b> で自分のドライブに複製<br />
                                                <span className="text-slate-500">※ 以降はこの「コピー」で作業します（これが自分のマスターになります）</span>
                                              </span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">3</span>
                                              <span>コピーしたシートで <b>拡張機能 → Apps Script</b></span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">4</span>
                                              <span>
                                                <b>コード.gs</b>（既定で開いている）の中身を<b>全部消して</b>貼り付け
                                                <button onClick={async () => {
                                                  try {
                                                    const r = await fetch('/docs/hearing-gas.js')
                                                    await navigator.clipboard.writeText(await r.text())
                                                    alert('✅ コード.gs をコピーしました\\n\\nApps Scriptの「コード.gs」を全選択(Ctrl+A)して削除してから貼り付けてください')
                                                  } catch { alert('コピー失敗') }
                                                }}
                                                  className="ml-1 px-2 py-0.5 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                                  📋 コード.gs をコピー
                                                </button>
                                              </span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">5</span>
                                              <span>
                                                左サイドの<b>「ファイル」の横の ＋</b> → <b>HTML</b> を選択<br />
                                                ファイル名は <b className="text-amber-300">dialog</b>（.html は付けない）<br />
                                                <span className="text-slate-500">※ コード側がこの名前で呼ぶので、必ず dialog にしてください</span>
                                                <button onClick={async () => {
                                                  try {
                                                    const r = await fetch('/docs/hearing-gas-dialog.html')
                                                    await navigator.clipboard.writeText(await r.text())
                                                    alert('✅ dialog.html をコピーしました\\n\\n作成した dialog ファイルの中身を全部消してから貼り付けてください')
                                                  } catch { alert('コピー失敗') }
                                                }}
                                                  className="ml-1 px-2 py-0.5 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                                  📋 dialog.html をコピー
                                                </button>
                                              </span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">6</span>
                                              <span><b>Ctrl + S</b> で保存（左上の「変更が保存されていません」が消える）</span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">7</span>
                                              <span>コピーしたスプレッドシートのタブに戻り <b>F5 で再読み込み</b></span>
                                            </div>
                                          </div>

"""
s = s[:i] + NEW + s[j:]
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
