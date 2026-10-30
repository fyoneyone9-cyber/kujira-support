# -*- coding: utf-8 -*-
"""[HEARING_GAS_V5 2026-10-29] Googleアカウント切り替えに対応する。

症状: 「雛形のコピーを作る」で "Sorry, unable to open the file at this time."
真因: ブラウザに複数のGoogleアカウントがログインしており、既定アカウント(u/0)では
      雛形にアクセスできない。実際に使っているのは authuser=2。

対策: URLに /u/2/ を入れてアカウントを明示する。
      さらに u/0〜u/3 を選べるボタンも並べ、環境が変わっても自力で切り替えられるようにする。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_authuser_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                                <a href={TMPL.replace(/\\/edit.*$/, '/copy')} target="_blank" rel="noreferrer"
                                                  className="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold">
                                                  🔗 雛形のコピーを作る（クリック）
                                                </a>
                                                <br />
                                                <span className="text-slate-500">開いた画面で「コピーを作成」を押す → 自分のドライブに複製されます</span>"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                                {/* [HEARING_GAS_V5 2026-10-29] 複数Googleアカウントでログインしていると
                                                    既定(u/0)では開けず "unable to open the file" になる。
                                                    実際に使っているのは authuser=2 なので u/2 を既定にし、
                                                    他のアカウントも選べるようにしておく。 */}
                                                {(() => {
                                                  const id = (TMPL.match(/\\/d\\/([^/]+)/) || [])[1] || ''
                                                  const url = (u: number) => `https://docs.google.com/spreadsheets/u/${u}/d/${id}/copy`
                                                  return (
                                                    <>
                                                      <a href={url(2)} target="_blank" rel="noreferrer"
                                                        className="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold">
                                                        🔗 雛形のコピーを作る（クリック）
                                                      </a>
                                                      <span className="ml-2 text-slate-400">開けない場合は別アカウントで:</span>
                                                      {[0, 1, 2, 3].map(u => (
                                                        <a key={u} href={url(u)} target="_blank" rel="noreferrer"
                                                          className="ml-1 px-2 py-0.5 rounded bg-slate-700 hover:bg-slate-600 text-slate-200">
                                                          u/{u}
                                                        </a>
                                                      ))}
                                                      <br />
                                                      <span className="text-slate-500">開いた画面で「コピーを作成」を押す → 自分のドライブに複製されます</span>
                                                    </>
                                                  )
                                                })()}"""
s = s.replace(OLD, NEW, 1)

# 「雛形を開く」リンクも u/2 にする
OLD2 = """                                  <a href={TMPL} target="_blank" rel="noreferrer"
                                    className="text-sm px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold transition-colors">
                                    📄 雛形を開く
                                  </a>"""
if s.count(OLD2) == 1:
    NEW2 = """                                  <a href={TMPL.replace('/spreadsheets/d/', '/spreadsheets/u/2/d/')} target="_blank" rel="noreferrer"
                                    className="text-sm px-2.5 py-1 rounded bg-emerald-700 hover:bg-emerald-600 text-white font-bold transition-colors">
                                    📄 雛形を開く
                                  </a>"""
    s = s.replace(OLD2, NEW2, 1)
    print("雛形を開くリンクも u/2 に変更")

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
