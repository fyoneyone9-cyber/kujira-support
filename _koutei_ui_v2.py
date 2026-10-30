# -*- coding: utf-8 -*-
"""[KOUTEI_GAS_UI_V2 2026-10-29] 工程管理の導線を親切にする（行番号指定で安全に置換）。

指摘:「不親切すぎ」
  文字が並んでいるだけで、どこを押せばいいか分からなかった。
  ヒアリングシートと同じく、各手順にボタンを付ける。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_kui3_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
L = io.open(P, encoding="utf-8").read().split("\n")

# L2316(index 2315) から L2354(index 2353) までを置換
s_idx, e_idx = 2315, 2354
assert "KOUTEI_GAS_UI_V1" in L[s_idx], "start mismatch: %r" % L[s_idx][:60]
assert L[e_idx - 1].strip() == "</div>", "end mismatch: %r" % L[e_idx - 1]

KV = re.search(r"var KOUTEI_VERSION = '([^']*)'",
               io.open(r"C:\GensparkClaw\kujira-support\public\docs\koutei-gas.js",
                       encoding="utf-8").read()).group(1)

I = " " * 36
BLOCK = '''{I}{{/* [KOUTEI_GAS_UI_V2 2026-10-29] 手順にボタンを付けて迷わないようにする */}}
{I}<div className="mt-2 pt-2 border-t border-slate-700/50">
{I}  <div className="flex items-center gap-2 flex-wrap">
{I}    <span className="text-base text-emerald-300 font-bold">⭐ スプレッドシートで作る（推奨）</span>
{I}    <span className="text-sm px-2 py-1 rounded bg-slate-800 border border-slate-600 text-slate-300 font-mono">最新: {KV}</span>
{I}  </div>

{I}  {{/* 毎回やること（常時表示） */}}
{I}  <div className="mt-2 bg-slate-900/60 border border-amber-800/50 rounded-lg p-2.5">
{I}    <p className="text-base font-bold text-amber-300 mb-1.5">▶ 作成手順（毎回これだけ）</p>
{I}    <div className="space-y-2 text-sm text-slate-300 leading-relaxed">
{I}      <div className="flex gap-2 items-start">
{I}        <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">1</span>
{I}        <span className="flex items-center gap-2 flex-wrap">
{I}          <span>設定をコピー（会社名・機材構成）</span>
{I}          <button onClick={{() => {{
{I}            const b = document.querySelector<HTMLButtonElement>(`[data-cfgcopy="${{it.id}}"]`)
{I}            b?.click()
{I}          }}}} className="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold">📋 設定をコピー</button>
{I}        </span>
{I}      </div>
{I}      <div className="flex gap-2 items-start">
{I}        <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">2</span>
{I}        <span className="flex items-center gap-2 flex-wrap">
{I}          <span>自分の工程表を開き <b className="text-amber-300">🗂 工程管理 → 必要な工程だけコピー作成</b></span>
{I}          {{((): React.ReactNode => {{
{I}            const mine = (it.dashboard_todos?.['my_koutei_url'] as string) || ''
{I}            if (mine) return (
{I}              <a href={{mine}} target="_blank" rel="noreferrer" className="px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">📄 自分の工程表を開く</a>
{I}            )
{I}            return (
{I}              <button onClick={{() => {{
{I}                const u = prompt('自分がコピーした工程管理表のURLを貼り付けてください')
{I}                if (u && u.startsWith('http')) saveTodoKey(it.id, it.dashboard_todos, 'my_koutei_url', u.trim())
{I}              }}}} className="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">➕ 工程表のURLを登録</button>
{I}            )
{I}          }})()}}
{I}        </span>
{I}      </div>
{I}      <div className="flex gap-2 items-start">
{I}        <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">3</span>
{I}        <span>一番上の欄に <b>貼り付け</b> → <b className="text-amber-300">⬇ 反映</b> → <b className="text-emerald-300">コピーを作成</b><br /><span className="text-slate-500">不要な工程行が自動で削除されます</span></span>
{I}      </div>
{I}    </div>
{I}  </div>

{I}  {{/* 初回だけの設置手順 */}}
{I}  {{((): React.ReactNode => {{
{I}    const gk = `kgas_${{it.id}}`
{I}    const op = openSections[gk]
{I}    return (
{I}      <div className="mt-2">
{I}        <button onClick={{() => toggleSection(gk)}} className="text-sm px-2.5 py-1 rounded bg-emerald-900/50 hover:bg-emerald-800 border border-emerald-700 text-emerald-200 font-bold">
{I}          {{op ? '▲ 設置手順を閉じる' : '❓ 初回だけの設置手順を見る（2分）'}}
{I}        </button>
{I}        {{op && (
{I}          <div className="mt-2 bg-slate-900/70 border border-emerald-800/50 rounded-lg p-3 space-y-2">
{I}            <div className="bg-rose-950/40 border border-rose-700/60 rounded px-2 py-1.5">
{I}              <p className="text-sm text-rose-200 font-bold">⚠ コード.gs と dialog_koutei は必ず両方セットで貼ってください</p>
{I}            </div>
{I}            <div className="space-y-2 text-sm text-slate-300 leading-relaxed">
{I}              <div className="flex gap-2 items-start">
{I}                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-xs">1</span>
{I}                <span className="flex items-center gap-2 flex-wrap">
{I}                  <span>原本をコピーして自分のものを作る</span>
{I}                  <a href="https://docs.google.com/spreadsheets/u/2/d/1GiEvK-KLB7rl1lrCn-Llgl9H6W4m2PuZJXby2RqIuMc/copy" target="_blank" rel="noreferrer" className="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold">🔗 原本のコピーを作る</a>
{I}                </span>
{I}              </div>
{I}              <div className="flex gap-2 items-start">
{I}                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">2</span>
{I}                <span>コピーしたシートで <b>拡張機能 → Apps Script</b></span>
{I}              </div>
{I}              <div className="flex gap-2 items-start">
{I}                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">3</span>
{I}                <span className="flex items-center gap-2 flex-wrap">
{I}                  <span><b>コード.gs</b> を全消し(Ctrl+A→Del)して貼り付け</span>
{I}                  <button onClick={{async () => {{
{I}                    try {{
{I}                      const r = await fetch('/api/delivery/gas-source?f=koutei&t=' + Date.now(), {{ cache: 'no-store' }})
{I}                      const t = await r.text()
{I}                      if (!t.includes('createKouteiCopy')) {{ alert('⚠ 取得に失敗。Ctrl+Shift+R で再読込してください'); return }}
{I}                      await navigator.clipboard.writeText(t)
{I}                      alert('✅ コード.gs をコピーしました（' + t.length.toLocaleString() + '文字）')
{I}                    }} catch {{ alert('コピー失敗') }}
{I}                  }}}} className="px-2.5 py-1 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">📋 コード.gs をコピー</button>
{I}                </span>
{I}              </div>
{I}              <div className="flex gap-2 items-start">
{I}                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">4</span>
{I}                <span className="flex items-center gap-2 flex-wrap">
{I}                  <span>左の <b>＋ → HTML</b>、ファイル名は <b className="text-amber-300">dialog_koutei</b><span className="text-slate-500">（.html は付けない）</span></span>
{I}                  <button onClick={{async () => {{
{I}                    try {{
{I}                      const r = await fetch('/api/delivery/gas-source?f=koutei-dialog&t=' + Date.now(), {{ cache: 'no-store' }})
{I}                      const t = await r.text()
{I}                      if (!t.includes('createKouteiCopy')) {{ alert('⚠ 取得に失敗。Ctrl+Shift+R で再読込してください'); return }}
{I}                      await navigator.clipboard.writeText(t)
{I}                      alert('✅ dialog_koutei をコピーしました（' + t.length.toLocaleString() + '文字）\\n\\nファイル名は必ず dialog_koutei にしてください')
{I}                    }} catch {{ alert('コピー失敗') }}
{I}                  }}}} className="px-2.5 py-1 rounded bg-blue-700 hover:bg-blue-600 text-white font-bold">📋 dialog_koutei をコピー</button>
{I}                </span>
{I}              </div>
{I}              <div className="flex gap-2 items-start">
{I}                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">5</span>
{I}                <span><b>Ctrl + S</b> で保存 → スプレッドシートに戻って <b>F5</b></span>
{I}              </div>
{I}              <div className="flex gap-2 items-start">
{I}                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-xs">6</span>
{I}                <span>メニューに <b className="text-amber-300">🗂 工程管理</b> が出たら完了<br /><span className="text-slate-500">「🔑 権限を承認する」を一度実行してください</span></span>
{I}              </div>
{I}            </div>
{I}            <p className="text-sm text-emerald-400 pt-1 border-t border-slate-700">原本をコピーして不要行を消す方式なので、書式・色・条件付き書式がそのまま残ります</p>
{I}          </div>
{I}        )}}
{I}      </div>
{I}    )
{I}  }})()}}
{I}</div>'''.format(I=I, KV=KV)

L[s_idx:e_idx] = BLOCK.split("\n")
io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("patched OK (L%d-%d を置換)" % (s_idx + 1, e_idx))
