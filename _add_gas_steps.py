# -*- coding: utf-8 -*-
"""[HEARING_GAS_V2 2026-10-29] Apps Script の設置手順をUIに表示する。
リンクを並べるだけでは何をすればいいか分からないので、
番号付きの手順＋コードをその場でコピーできるボタンを出す。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_gassteps_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                                  初回のみ: 雛形を開く → 拡張機能 → Apps Script → 上記2ファイルを貼付して保存<br />
                                  以降: 雛形のメニュー「📋 ヒアリングシート」→「必要シートだけコピー作成」<br />
                                  <span className="text-emerald-400">雛形をコピーして不要シートを消す方式なので、書式・結合・色が完全に一致します</span>
                                </p>"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                {/* [HEARING_GAS_V2 2026-10-29] 設置手順をその場に表示する */}
                                {(() => {
                                  const gasKey = `gas_${it.id}`
                                  const open = openSections[gasKey]
                                  return (
                                    <div className="mt-1">
                                      <button onClick={() => toggleSection(gasKey)}
                                        className="text-[11px] px-2 py-1 rounded bg-emerald-900/50 hover:bg-emerald-800 border border-emerald-700 text-emerald-200 font-bold transition-colors">
                                        {open ? '▲ 設置手順を閉じる' : '❓ 初回だけの設置手順を見る（2分）'}
                                      </button>
                                      {open && (
                                        <div className="mt-2 bg-slate-900/70 border border-emerald-800/50 rounded-lg p-3 space-y-2">
                                          <p className="text-[11px] text-emerald-300 font-bold">
                                            雛形をコピーして不要シートを消す方式です。書式・結合・色が元のまま残ります。
                                          </p>

                                          <div className="space-y-1.5 text-[11px] text-slate-300 leading-relaxed">
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">1</span>
                                              <span>上の <b className="text-emerald-300">📄 雛形を開く</b> をクリック</span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">2</span>
                                              <span>スプレッドシートのメニュー <b>拡張機能 → Apps Script</b></span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">3</span>
                                              <span>
                                                <b>コード.gs</b> の中身を全部消して、下のボタンでコピーしたコードを貼り付け
                                                <button onClick={async () => {
                                                  try {
                                                    const r = await fetch('/docs/hearing-gas.js')
                                                    await navigator.clipboard.writeText(await r.text())
                                                    alert('✅ コード.gs をコピーしました\\nApps Scriptに貼り付けてください')
                                                  } catch { alert('コピー失敗') }
                                                }}
                                                  className="ml-1 px-2 py-0.5 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                                  📋 コード.gs をコピー
                                                </button>
                                              </span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">4</span>
                                              <span>
                                                左の <b>＋ → HTML</b> を選び、ファイル名を <b className="text-amber-300">dialog</b> にして貼り付け
                                                <button onClick={async () => {
                                                  try {
                                                    const r = await fetch('/docs/hearing-gas-dialog.html')
                                                    await navigator.clipboard.writeText(await r.text())
                                                    alert('✅ dialog.html をコピーしました\\nファイル名を「dialog」にして貼り付けてください')
                                                  } catch { alert('コピー失敗') }
                                                }}
                                                  className="ml-1 px-2 py-0.5 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                                  📋 dialog.html をコピー
                                                </button>
                                              </span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">5</span>
                                              <span>💾 で保存 → 雛形のタブを<b>再読み込み</b></span>
                                            </div>
                                          </div>

                                          <div className="pt-2 border-t border-slate-700">
                                            <p className="text-[11px] text-amber-300 font-bold mb-1">✅ 設置が終わったら（毎回の操作）</p>
                                            <p className="text-[11px] text-slate-300 leading-relaxed">
                                              雛形のメニュー <b className="text-amber-300">📋 ヒアリングシート</b> →
                                              <b>「必要シートだけコピー作成」</b><br />
                                              会社名・機材にチェック → <b>コピーを作成</b> → 新しいシートのリンクが出ます
                                            </p>
                                          </div>
                                        </div>
                                      )}
                                    </div>
                                  )
                                })()}"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
