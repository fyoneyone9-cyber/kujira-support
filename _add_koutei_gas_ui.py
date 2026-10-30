# -*- coding: utf-8 -*-
"""[KOUTEI_GAS_UI_V1 2026-10-29] 工程管理表のApps Script導線を追加する。

要望:「工程管理表の精度あげてほしいのとスプシにしてほしい」
  Excel生成ではなく、原本スプレッドシートをコピーして
  不要な行を削除する方式にする（ヒアリングシートと同じ）。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_kgas_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

G = io.open(r"C:\GensparkClaw\kujira-support\public\docs\koutei-gas.js", encoding="utf-8").read()
ver = re.search(r"var KOUTEI_VERSION = '([^']*)'", G).group(1)

ANCHOR = """                                      <span className="text-sm text-slate-500">
                                        ※ 使わない機材の工程行を自動で削除します
                                      </span>"""
assert s.count(ANCHOR) == 1, "anchor: %d" % s.count(ANCHOR)

NEW = """                                      <span className="text-sm text-slate-500">
                                        ※ 使わない機材の工程行を自動で削除します
                                      </span>
                                    </div>

                                    {/* [KOUTEI_GAS_UI_V1 2026-10-29] スプレッドシート版（書式そのまま） */}
                                    <div className="mt-2 pt-2 border-t border-slate-700/50">
                                      <div className="flex items-center gap-2 flex-wrap">
                                        <span className="text-sm text-emerald-300 font-bold">⭐ スプレッドシートで作る（推奨）:</span>
                                        <span className="text-sm px-2 py-1 rounded bg-slate-800 border border-slate-600 text-slate-300 font-mono">
                                          最新: %s
                                        </span>
                                        <button onClick={async () => {
                                          try {
                                            const r = await fetch('/api/delivery/gas-source?f=koutei&t=' + Date.now(), { cache: 'no-store' })
                                            const t = await r.text()
                                            if (!t.includes('createKouteiCopy')) { alert('⚠ 取得に失敗。Ctrl+Shift+R で再読込してください'); return }
                                            await navigator.clipboard.writeText(t)
                                            alert(`✅ コード.gs をコピーしました（${t.length.toLocaleString()}文字）\\n\\n工程管理表のApps Scriptに貼り付けてください`)
                                          } catch { alert('コピー失敗') }
                                        }}
                                          className="text-sm px-2.5 py-1 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                          📋 コード.gs をコピー
                                        </button>
                                        <button onClick={async () => {
                                          try {
                                            const r = await fetch('/api/delivery/gas-source?f=koutei-dialog&t=' + Date.now(), { cache: 'no-store' })
                                            const t = await r.text()
                                            if (!t.includes('createKouteiCopy')) { alert('⚠ 取得に失敗。Ctrl+Shift+R で再読込してください'); return }
                                            await navigator.clipboard.writeText(t)
                                            alert(`✅ dialog_koutei をコピーしました（${t.length.toLocaleString()}文字）\\n\\nファイル名は「dialog_koutei」にしてください`)
                                          } catch { alert('コピー失敗') }
                                        }}
                                          className="text-sm px-2.5 py-1 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                          📋 dialog_koutei をコピー
                                        </button>
                                      </div>
                                      <p className="text-sm text-slate-400 mt-1.5 leading-relaxed">
                                        <b className="text-rose-300">⚠ 2ファイルとも貼り替えてください</b>（片方だけだと動きません）<br />
                                        初回: 工程管理表の原本を<b>コピー</b> → 拡張機能 → Apps Script → 上記2つを貼付 → Ctrl+S<br />
                                        以降: メニュー <b className="text-amber-300">🗂 工程管理 → 必要な工程だけコピー作成</b><br />
                                        <span className="text-emerald-400">原本をコピーして不要行を消すので、書式・色・条件付き書式がそのまま残ります</span>
                                      </p>
                                    </div>""" % ver

# 元の </div> を1つ消す（上で追加したため）
OLD_TAIL = ANCHOR + """
                                    </div>"""
assert s.count(OLD_TAIL) == 1, "tail anchor"
s = s.replace(OLD_TAIL, NEW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("工程管理のGAS導線を追加:", ver)
