# -*- coding: utf-8 -*-
"""[GAS_SOURCE_V1 2026-10-29] コード表示リンクを分かりやすくする。

指摘:「http://localhost:3001/docs/hearing-gas-dialog.html うごかねえよ」
  → これは Apps Script に貼る「ソースコード」であって、開いても動かない。
     ブラウザが HTML として解釈し、空白ページに見えていた。

対策:
  ・リンク先を text/plain を返す API に変更（コードがそのまま見える）
  ・ボタン名を「📜 コード.gs」→「👁 コードを見る」に変更し、
    主役は「📋 コピー」であることを明確にする
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_gaslink_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD = """                                  <a href="/docs/hearing-gas.js" target="_blank" rel="noreferrer"
                                    className="text-sm px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
                                    title="Apps Scriptに貼り付けるコード（初回のみ）">
                                    📜 コード.gs
                                  </a>
                                  <a href="/docs/hearing-gas-dialog.html" target="_blank" rel="noreferrer"
                                    className="text-sm px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
                                    title="Apps Scriptに貼り付けるHTML（初回のみ）">
                                    📜 dialog.html
                                  </a>"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                  {/* [GAS_SOURCE_V1 2026-10-29] これは「貼り付け用のソース」であって
                                      開いても動くページではない。text/plain で中身だけ見せる。 */}
                                  <a href="/api/delivery/gas-source?f=code" target="_blank" rel="noreferrer"
                                    className="text-sm px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
                                    title="Apps Scriptに貼り付けるコードの中身を表示します（確認用）">
                                    👁 コード.gs の中身
                                  </a>
                                  <a href="/api/delivery/gas-source?f=dialog" target="_blank" rel="noreferrer"
                                    className="text-sm px-2 py-1 rounded bg-slate-700 hover:bg-slate-600 text-slate-200 transition-colors"
                                    title="Apps Scriptに貼り付けるHTMLの中身を表示します（確認用）">
                                    👁 dialog の中身
                                  </a>"""
s = s.replace(OLD, NEW, 1)

# コピーボタンの取得先も API 経由に（キャッシュ回避）
s = s.replace("await fetch('/docs/hearing-gas.js')",
              "await fetch('/api/delivery/gas-source?f=code')")
s = s.replace("await fetch('/docs/hearing-gas-dialog.html')",
              "await fetch('/api/delivery/gas-source?f=dialog')")

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
