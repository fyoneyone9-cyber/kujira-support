# -*- coding: utf-8 -*-
"""[KOUTEI_GAS_UI_V2 2026-10-29] 工程管理表の導線を親切にする。

指摘:「不親切すぎ」
  文字が並んでいるだけで、どこを押せばいいか分からない。
  ヒアリングシート側と同じく、各手順にボタンを付ける。

やること:
  ・折りたたみ式の設置手順（番号付き・各ステップにボタン）
  ・「毎回やること」を常時表示
  ・原本コピーのリンクを /copy 付き & authuser=2 で直接開けるように
  ・自分の工程表URLを登録して、以後ワンクリックで開けるように
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_kui2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

start = s.index("                                    {/* [KOUTEI_GAS_UI_V1 2026-10-29] スプレッドシート版（書式そのまま） */}")
end = s.index("</div>", s.index("原本をコピーして不要行を消すので")) + len("</div>")
# その後の閉じタグまで含める
end = s.index("</div>", end) + len("</div>")

KV = re.search(r"var KOUTEI_VERSION = '([^']*)'",
               io.open(r"C:\GensparkClaw\kujira-support\public\docs\koutei-gas.js",
                       encoding="utf-8").read()).group(1)

NEW = """                                    {/* [KOUTEI_GAS_UI_V2 2026-10-29] 手順にボタンを付けて迷わないようにする */}
                                    <div className="mt-2 pt-2 border-t border-slate-700/50">
                                      <div className="flex items-center gap-2 flex-wrap">
                                        <span className="text-base text-emerald-300 font-bold">⭐ スプレッドシートで作る（推奨）</span>
                                        <span className="text-sm px-2 py-1 rounded bg-slate-800 border border-slate-600 text-slate-300 font-mono">
                                          最新: %s
                                        </span>
                                      </div>

                                      {/* 毎回やること（常時表示） */}
                                      <div className="mt-2 bg-slate-900/60 border border-amber-800/50 rounded-lg p-2.5">
                                        <p className="text-base font-bold text-amber-300 mb-1.5">▶ 作成手順（毎回これだけ）</p>
                                        <div className="space-y-2 text-sm text-slate-300 leading-relaxed">
                                          <div className="flex gap-2 items-start">
                                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">1</span>
                                            <span className="flex items-center gap-2 flex-wrap">
                                              <span>設定をコピー（会社名・機材構成）</span>
                                              <button onClick={() => {
                                                const btn = document.querySelector<HTMLButtonElement>(`[data-cfgcopy="${it.id}"]`)
                                                btn?.click()
                                              }}
                                                className="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold">
                                                📋 設定をコピー
                                              </button>
                                            </span>
                                          </div>
                                          <div className="flex gap-2 items-start">
                                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">2</span>
                                            <span className="flex items-center gap-2 flex-wrap">
                                              <span>自分の工程管理表を開き、メニュー <b className="text-amber-300">🗂 工程管理 → 必要な工程だけコピー作成</b></span>
                                              {(() => {
                                                const mine = (it.dashboard_todos?.['my_koutei_url'] as string) || ''
                                                return mine ? (
                                                  <a href={mine} target="_blank" rel="noreferrer"
                                                    className="px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
                                                    📄 自分の工程表を開く
                                                  </a>
                                                ) : (
                                                  <button onClick={() => {
                                                    const u = prompt('自分がコピーした工程管理表のURLを貼り付けてください\\n（一度登録すれば次回からボタンで開けます）')
                                                    if (u && u.startsWith('http')) saveTodoKey(it.id, it.dashboard_todos, 'my_koutei_url', u.trim())
                                                  }}
                                                    className="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                                    ➕ 工程表のURLを登録
                                                  </button>
                                                )
                                              })()}
                                            </span>
                                          </div>
                                          <div className="flex gap-2 items-start">
                                            <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">3</span>
                                            <span>
                                              一番上の欄に <b>貼り付け</b> → <b className="text-amber-300">⬇ 反映</b> → <b className="text-emerald-300">コピーを作成</b><br />
                                              <span className="text-slate-500">不要な工程行が自動で削除されます</span>
                                            </span>
                                          </div>
                                        </div>
                                      </div>

                                      {/* 初回だけの設置手順（折りたたみ） */}
                                      {(() => {
                                        const k = `kgas_${it.id}`
                                        const open = openSections[k]
                                        return (
                                          <div className="mt-2">
                                            <button onClick={() => toggleSection(k)}
                                              className="text-sm px-2.5 py-1 rounded bg-emerald-900/50 hover:bg-emerald-800 border border-emerald-700 text-emerald-200 font-bold">
                                              {open ? '▲ 設置手順を閉じる' : '❓ 初回だけの設置手順を見る（2分）'}
                                            </button>
                                            {open && (
                                              <div className="mt-2 bg-slate-900/70 border border-emerald-800/50 rounded-lg p-3 space-y-2">
                                                <div className="bg-rose-950/40 border border-rose-700/60 rounded px-2 py-1.5">
                                                  <p className="text-sm text-rose-200 font-bold">
                                                    ⚠ コード.gs と dialog_koutei は必ず両方セットで貼ってください
                                                  </p>
                                                </div>
                                                <div className="space-y-2 text-sm text-slate-300 leading-relaxed">
                                                  <div className="flex gap-2 items-start">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">1</span>
                                                    <span className="flex items-center gap-2 flex-wrap">
                                                      <span>原本をコピーして自分のものを作る</span>
                                                      <a href="https://docs.google.com/spreadsheets/u/2/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/copy"
                                                        target="_blank" rel="noreferrer"
                                                        className="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold">
                                                        🔗 原本のコピーを作る
                                                      </a>
                                                    </span>
                                                  </div>
                                                  <div className="flex gap-2 items-start">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">2</span>
                                                    <span>コピーしたシートで <b>拡張機能 → Apps Script</b></span>
                                                  </div>
                                                  <div className="flex gap-2 items-start">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">3</span>
                                                    <span className="flex items-center gap-2 flex-wrap">
                                                      <span><b>コード.gs</b> を全消し(Ctrl+A→Del)して貼り付け</span>
                                                      <button onClick={async () => {
                                                        try {
                                                          const r = await fetch('/api/delivery/gas-source?f=koutei&t=' + Date.now(), { cache: 'no-store' })
                                                          const t = await r.text()
                                                          if (!t.includes('createKouteiCopy')) { alert('⚠ 取得に失敗。Ctrl+Shift+R で再読込してください'); return }
                                                          await navigator.clipboard.writeText(t)
                                                          alert(`✅ コード.gs をコピーしました（${t.length.toLocaleString()}文字）`)
                                                        } catch { alert('コピー失敗') }
                                                      }}
                                                        className="px-2.5 py-1 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                                        📋 コード.gs をコピー
                                                      </button>
                                                    </span>
                                                  </div>
                                                  <div className="flex gap-2 items-start">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">4</span>
                                                    <span className="flex items-center gap-2 flex-wrap">
                                                      <span>
                                                        左の <b>＋ → HTML</b>、ファイル名は <b className="text-amber-300">dialog_koutei</b>
                                                        <span className="text-slate-500">（.html は付けない）</span>
                                                      </span>
                                                      <button onClick={async () => {
                                                        try {
                                                          const r = await fetch('/api/delivery/gas-source?f=koutei-dialog&t=' + Date.now(), { cache: 'no-store' })
                                                          const t = await r.text()
                                                          if (!t.includes('createKouteiCopy')) { alert('⚠ 取得に失敗。Ctrl+Shift+R で再読込してください'); return }
                                                          await navigator.clipboard.writeText(t)
                                                          alert(`✅ dialog_koutei をコピーしました（${t.length.toLocaleString()}文字）\\n\\nファイル名は必ず「dialog_koutei」にしてください`)
                                                        } catch { alert('コピー失敗') }
                                                      }}
                                                        className="px-2.5 py-1 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">
                                                        📋 dialog_koutei をコピー
                                                      </button>
                                                    </span>
                                                  </div>
                                                  <div className="flex gap-2 items-start">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">5</span>
                                                    <span><b>Ctrl + S</b> で保存 → スプレッドシートに戻って <b>F5</b></span>
                                                  </div>
                                                  <div className="flex gap-2 items-start">
                                                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">6</span>
                                                    <span>
                                                      メニューに <b className="text-amber-300">🗂 工程管理</b> が出たら完了<br />
                                                      <span className="text-slate-500">「🔑 権限を承認する」を一度実行してください</span>
                                                    </span>
                                                  </div>
                                                </div>
                                                <p className="text-sm text-emerald-400 pt-1 border-t border-slate-700">
                                                  原本をコピーして不要行を消す方式なので、書式・色・条件付き書式がそのまま残ります
                                                </p>
                                              </div>
                                            )}
                                          </div>
                                        )
                                      })()}
                                    </div>""" % KV

s = s[:start] + NEW + s[end:]
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
