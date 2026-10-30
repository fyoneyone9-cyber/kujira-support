# -*- coding: utf-8 -*-
"""[HEARING_GAS_V14 2026-10-29] 「設置が終わったら」の手順にボタンを付ける。

指摘:「ボタン付けれるところはつけろや」
  ⓪設定をコピー / ①シートを開く が文字だけで、わざわざ上までスクロールして
  探す必要があった。その場で押せるようにする。

付けるもの:
  ⓪ 📋 設定をコピー（上と同じ動作）
  ① 📄 自分のシートを開く（保存した自分のコピーのURL。未登録なら登録を促す）
  ⑤ 📁 マイドライブを開く（作成物の保存先）
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_stepbtn_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                              <p className="text-amber-200">
                                                ⓪ 上の <b>📋 設定をコピー</b> を押す（会社名と機材チェックが入ります）
                                              </p>
                                              <p>
                                                ① コピーしたシートのメニュー
                                                <b className="text-amber-300"> 📋 ヒアリングシート</b>（ヘルプの右隣）をクリック
                                              </p>"""
assert s.count(OLD) == 1, "anchor1: %d" % s.count(OLD)

NEW = """                                              <p className="text-amber-200 flex items-center gap-2 flex-wrap">
                                                <span>⓪ 設定をコピー（会社名と機材チェックが入ります）</span>
                                                <button onClick={() => {
                                                  const btn = document.querySelector<HTMLButtonElement>(`[data-cfgcopy="${it.id}"]`)
                                                  btn?.click()
                                                }}
                                                  className="px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold">
                                                  📋 設定をコピー
                                                </button>
                                              </p>
                                              <p className="flex items-center gap-2 flex-wrap">
                                                <span>
                                                  ① 自分のシートを開き、メニュー
                                                  <b className="text-amber-300"> 📋 ヒアリングシート</b>（ヘルプの右隣）
                                                </span>
                                                {(() => {
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
                                                })()}
                                              </p>"""
s = s.replace(OLD, NEW, 1)

OLD2 = """                                              <p>
                                                ⑤ <b>▶ 作成したスプレッドシートを開く</b> のリンクが出るのでクリック<br />
                                                <span className="text-slate-500">保存先: マイドライブ直下 / ファイル名「ヒアリングシート_会社名_日付」</span>
                                              </p>"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """                                              <p className="flex items-center gap-2 flex-wrap">
                                                <span>
                                                  ⑤ <b>▶ 作成したシートを開く</b> のリンクが出るのでクリック<br />
                                                  <span className="text-slate-500">保存先: マイドライブ直下「ヒアリングシート_会社名_日付」</span>
                                                </span>
                                                <a href="https://drive.google.com/drive/u/2/my-drive" target="_blank" rel="noreferrer"
                                                  className="px-2.5 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 font-bold">
                                                  📁 マイドライブ
                                                </a>
                                              </p>"""
s = s.replace(OLD2, NEW2, 1)

# 上の「設定をコピー」ボタンに data 属性を付けて、下から押せるようにする
OLD3 = """                                    className="text-sm px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold transition-colors"
                                    title="この案件の情報と機材チェックをまとめてコピーします">"""
assert s.count(OLD3) == 1, "anchor3"
NEW3 = """                                    data-cfgcopy={it.id}
                                    className="text-sm px-2.5 py-1 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold transition-colors"
                                    title="この案件の情報と機材チェックをまとめてコピーします">"""
s = s.replace(OLD3, NEW3, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
