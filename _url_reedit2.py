# -*- coding: utf-8 -*-
"""[MY_URL_EDIT_V1 2026-10-29] 登録したURLを変更・削除できるようにする（行指定）。

指摘:「登録し直しも出来るようにしてもらわないと困る」
  一度登録すると「📄 開く」だけになり、変更手段が無かった。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_urledit2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
L = io.open(P, encoding="utf-8").read().split("\n")


def block(indent, key, label, opentxt):
    I = " " * indent
    return '''{I}{{((): React.ReactNode => {{
{I}  // [MY_URL_EDIT_V1 2026-10-29] 登録済みでも ✏ から変更・解除できる
{I}  const mine = (it.dashboard_todos?.['{key}'] as string) || ''
{I}  const edit = () => {{
{I}    const u = prompt('{label}\\n（空にすると登録を解除します）', mine)
{I}    if (u === null) return
{I}    const v = u.trim()
{I}    if (v && !v.startsWith('http')) {{ alert('URLが正しくありません'); return }}
{I}    saveTodoKey(it.id, it.dashboard_todos, '{key}', v)
{I}  }}
{I}  if (mine) return (
{I}    <>
{I}      <a href={{mine}} target="_blank" rel="noreferrer" className="px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold">{opentxt}</a>
{I}      <button onClick={{edit}} title="登録したURLを変更・解除します" className="px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">✏ 変更</button>
{I}    </>
{I}  )
{I}  return (
{I}    <button onClick={{edit}} className="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">➕ URLを登録</button>
{I}  )
{I}}})()}}'''.format(I=I, key=key, label=label, opentxt=opentxt).split("\n")


# 後ろから置換（行番号がズレないように）
# ヒアリング: L2137-2153 (index 2136..2152)
assert "my_sheet_url" in L[2137], "hearing mismatch: %r" % L[2137][:60]
L[2136:2153] = block(48, "my_sheet_url",
                     "自分のコピーしたスプレッドシートのURLを貼り付けてください",
                     "📄 自分のシートを開く")
print("ヒアリング側 置換OK")

io.open(P, "w", encoding="utf-8").write("\n".join(L))

# 工程管理は行がズレたので再読込して処理
L = io.open(P, encoding="utf-8").read().split("\n")
hits = [i for i, l in enumerate(L) if "my_koutei_url" in l]
assert hits, "koutei not found"
st = hits[0] - 1          # {((): React.ReactNode => { の行
assert "React.ReactNode" in L[st], "koutei start mismatch: %r" % L[st][:60]
en = st
while "})()}" not in L[en]:
    en += 1
en += 1
L[st:en] = block(46, "my_koutei_url",
                 "自分がコピーした工程管理表のURLを貼り付けてください",
                 "📄 自分の工程表を開く")
print("工程管理側 置換OK (L%d-%d)" % (st + 1, en))

io.open(P, "w", encoding="utf-8").write("\n".join(L))
print("patched OK")
