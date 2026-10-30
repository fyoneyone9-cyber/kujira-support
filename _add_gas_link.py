# -*- coding: utf-8 -*-
"""[HEARING_GAS_V1 2026-10-29] Apps Script方式の導線を追加する。

経緯: CSVには結合・色・列幅の情報が無く、Excel生成では雛形と同じ見た目にできない。
      → 雛形スプレッドシートを丸ごとコピーして不要シートを削除する方式に変更。
         書式が完全に残るので一致する。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_gas_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

ANCHOR = """                              <span className="text-[11px] text-slate-500">
                                ※ Excelをドライブにドラッグ → 右クリック「Googleスプレッドシートで開く」
                              </span>"""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = """                              <span className="text-[11px] text-slate-500">
                                ※ Excelをドライブにドラッグ → 右クリック「Googleスプレッドシートで開く」
                              </span>
                              {/* [HEARING_GAS_V1 2026-10-29] Apps Script方式（書式が完全一致） */}
                              <div className="w-full mt-2 pt-2 border-t border-emerald-800/40">
                                <div className="flex items-center gap-1.5 flex-wrap">
                                  <span className="text-[11px] text-emerald-300 font-bold">⭐ 書式そのままコピー（推奨）:</span>
                                  <a href={TMPL} target="_blank" rel="noreferrer"
                                    className="text-[11px] px-2 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold transition-colors">
                                    📄 雛形を開く
                                  </a>
                                  <a href="/docs/hearing-gas.js" target="_blank" rel="noreferrer"
                                    className="text-[11px] px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
                                    title="Apps Scriptに貼り付けるコード（初回のみ）">
                                    📜 コード.gs
                                  </a>
                                  <a href="/docs/hearing-gas-dialog.html" target="_blank" rel="noreferrer"
                                    className="text-[11px] px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
                                    title="Apps Scriptに貼り付けるHTML（初回のみ）">
                                    📜 dialog.html
                                  </a>
                                </div>
                                <p className="text-[11px] text-slate-500 mt-1 leading-relaxed">
                                  初回のみ: 雛形を開く → 拡張機能 → Apps Script → 上記2ファイルを貼付して保存<br />
                                  以降: 雛形のメニュー「📋 ヒアリングシート」→「必要シートだけコピー作成」<br />
                                  <span className="text-emerald-400">雛形をコピーして不要シートを消す方式なので、書式・結合・色が完全に一致します</span>
                                </p>
                              </div>"""
s = s.replace(ANCHOR, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
