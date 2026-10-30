# -*- coding: utf-8 -*-
"""[DRIVE_LINK_V1 2026-10-29] Excel作成ボタンの隣にGoogleドライブへのリンクを追加する。

意図: DLした .xlsx を Googleドライブにアップすればスプレッドシートになる。
      その導線をボタン群のすぐ横に置いて、作業を途切れさせない。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_drivelink_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                📥 Excelで作成（{hearingSheets.length}枚）
                              </button>"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                📥 Excelで作成（{hearingSheets.length}枚）
                              </button>
                              {/* [DRIVE_LINK_V1 2026-10-29] DLしたxlsxをGoogleドライブに
                                  アップすればスプレッドシートになる。その導線をすぐ横に置く。 */}
                              <a href="https://drive.google.com/drive/my-drive" target="_blank" rel="noreferrer"
                                className="flex items-center gap-1.5 px-3 py-1.5 bg-yellow-600 hover:bg-yellow-500 text-white text-xs rounded-lg font-bold transition-colors"
                                title="ダウンロードしたExcelをここにドラッグ＆ドロップ → 右クリック「Googleスプレッドシートで開く」">
                                📁 Googleドライブ
                              </a>
                              <a href={TMPL} target="_blank" rel="noreferrer"
                                className="flex items-center gap-1.5 px-3 py-1.5 bg-purple-900/60 hover:bg-purple-800 border border-purple-700 text-purple-200 text-xs rounded-lg font-bold transition-colors"
                                title="元の雛形スプレッドシートを開きます">
                                📄 雛形を開く
                              </a>
                              <span className="text-[11px] text-slate-500">
                                ※ Excelをドライブにドラッグ → 右クリック「Googleスプレッドシートで開く」
                              </span>"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
