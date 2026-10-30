# -*- coding: utf-8 -*-
"""[MY_URL_EDIT_V1 2026-10-29] 登録したURLを変更・削除できるようにする。

指摘:「登録し直しも出来るようにしてもらわないと困る」
  一度登録すると「📄 開く」ボタンになり、変更手段が無かった。

対策: 登録済みのときも ✏ ボタンを出し、
  ・変更（現在値を初期値にした prompt）
  ・空にすれば登録解除
  ができるようにする。ヒアリング側(my_sheet_url)も同じ。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_urledit_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

# ---------- 工程管理表 ----------
OLD = """                                          {((): React.ReactNode => {
                                            const mine = (it.dashboard_todos?.['my_koutei_url'] as string) || ''
                                            if (mine) return (
                                              <a href={mine} target="_blank" rel="noreferrer" className="px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">📄 自分の工程表を開く</a>
                                            )
                                            return (
                                              <button onClick={() => {
                                                const u = prompt('自分がコピーした工程管理表のURLを貼り付けてください')
                                                if (u && u.startsWith('http')) saveTodoKey(it.id, it.dashboard_todos, 'my_koutei_url', u.trim())
                                              }} className="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">➕ 工程表のURLを登録</button>
                                            )
                                          })()}"""
assert s.count(OLD) == 1, "anchor1: %d" % s.count(OLD)

NEW = """                                          {((): React.ReactNode => {
                                            // [MY_URL_EDIT_V1] 登録済みでも変更・解除できるようにする
                                            const mine = (it.dashboard_todos?.['my_koutei_url'] as string) || ''
                                            const edit = () => {
                                              const u = prompt(
                                                '自分がコピーした工程管理表のURLを貼り付けてください\\n（空にすると登録を解除します）',
                                                mine)
                                              if (u === null) return            // キャンセル
                                              const v = u.trim()
                                              if (v && !v.startsWith('http')) { alert('URLが正しくありません'); return }
                                              saveTodoKey(it.id, it.dashboard_todos, 'my_koutei_url', v)
                                            }
                                            if (mine) return (
                                              <>
                                                <a href={mine} target="_blank" rel="noreferrer"
                                                  className="px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
                                                  📄 自分の工程表を開く
                                                </a>
                                                <button onClick={edit} title="登録したURLを変更・解除します"
                                                  className="px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">
                                                  ✏ 変更
                                                </button>
                                              </>
                                            )
                                            return (
                                              <button onClick={edit}
                                                className="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                                ➕ 工程表のURLを登録
                                              </button>
                                            )
                                          })()}"""
s = s.replace(OLD, NEW, 1)

# ---------- ヒアリングシート ----------
OLD2 = """                                                {(() => {
                                                  const mine = (it.dashboard_todos?.['my_sheet_url'] as string) || ''
                                                  return mine ? (
                                                    <a href={mine} target="_blank" rel="noreferrer"
                                                      className="px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
                                                      📄 自分のシートを開く
                                                    </a>
                                                  ) : (
                                                    <button onClick={() => {
                                                      const u = prompt('自分のコピーしたスプレッドシートのURLを貼り付けてください\\n（一度登録すれば次回からボタンで開けます）')
                                                      if (u && u.startsWith('http')) saveTodoKey(it.id, it.dashboard_todos, 'my_sheet_url', u.trim())
                                                    }}
                                                      className="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                                      ➕ 自分のシートURLを登録
                                                    </button>
                                                  )
                                                })()}"""
if s.count(OLD2) == 1:
    NEW2 = """                                                {((): React.ReactNode => {
                                                  // [MY_URL_EDIT_V1] 登録済みでも変更・解除できるようにする
                                                  const mine = (it.dashboard_todos?.['my_sheet_url'] as string) || ''
                                                  const edit = () => {
                                                    const u = prompt(
                                                      '自分のコピーしたスプレッドシートのURLを貼り付けてください\\n（空にすると登録を解除します）',
                                                      mine)
                                                    if (u === null) return
                                                    const v = u.trim()
                                                    if (v && !v.startsWith('http')) { alert('URLが正しくありません'); return }
                                                    saveTodoKey(it.id, it.dashboard_todos, 'my_sheet_url', v)
                                                  }
                                                  if (mine) return (
                                                    <>
                                                      <a href={mine} target="_blank" rel="noreferrer"
                                                        className="px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">
                                                        📄 自分のシートを開く
                                                      </a>
                                                      <button onClick={edit} title="登録したURLを変更・解除します"
                                                        className="px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">
                                                        ✏ 変更
                                                      </button>
                                                    </>
                                                  )
                                                  return (
                                                    <button onClick={edit}
                                                      className="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                                      ➕ 自分のシートURLを登録
                                                    </button>
                                                  )
                                                })()}"""
    s = s.replace(OLD2, NEW2, 1)
    print("  ヒアリングシート側も対応")

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
