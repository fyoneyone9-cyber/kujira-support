# -*- coding: utf-8 -*-
"""[HEARING_XLSX_V1] Geminiを使わずExcelを直接ダウンロードするボタンを追加する。

経緯: Geminiにプロンプトを渡しても「Googleドライブに空ファイルを作る」だけで、
      各シートへの書き込みができず、CSVを手で貼り付ける作業が発生していた。
      → サーバーで .xlsx を生成して直接DLさせる方式に変更。
         Googleドライブにアップすればそのままスプレッドシートになる。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_xlsxbtn_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-700 hover:bg-emerald-600 text-white text-xs rounded-lg font-bold transition-colors"
                                title="雛形から必要なシートだけを抜き出した新規スプレッドシートをGeminiに作らせます"
                              >
                                📝 必要シートだけ作成（{hearingSheets.length}枚）
                              </button>"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)

NEW = """                                className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-white text-xs rounded-lg font-bold transition-colors"
                                title="Gemini用のプロンプトをコピーします（Excelを直接作るなら左のボタンが確実です）"
                              >
                                🤖 Gemini用プロンプト（{hearingSheets.length}枚）
                              </button>
                              {/* [HEARING_XLSX_V1 2026-10-29] Geminiはスプレッドシートを作れないため、
                                  サーバーで.xlsxを生成して直接ダウンロードする。
                                  Googleドライブにアップすればそのままスプレッドシートになる。 */}
                              <button
                                onClick={async () => {
                                  try {
                                    const res = await fetch('/api/delivery/hearing-xlsx', {
                                      method: 'POST',
                                      headers: { 'Content-Type': 'application/json' },
                                      body: JSON.stringify({
                                        sheets: hearingSheets.map(x => x.label),
                                        info: {
                                          client: it.client_name || '',
                                          address: it.install_address || '',
                                          contact: it.contact_name || '',
                                          due: it.delivery_due_date || '',
                                          equipment: equip.map((e: Equipment) => [e.name, e.value].filter(Boolean).join(' ')).join('、'),
                                        },
                                        prefill: {
                                          'スマートロック': hasLock2 ? 'TRUE' : 'FALSE',
                                          'カードキー': hasCard ? 'TRUE' : 'FALSE',
                                          'シリンダー錠': hasCyli ? 'TRUE' : 'FALSE',
                                          'PMS': hasPms2 ? 'TRUE' : 'FALSE',
                                          'プリンタ': hasPrinter ? 'TRUE' : 'FALSE',
                                          'ルームタブレット': hasTablet ? 'TRUE' : 'FALSE',
                                        },
                                      }),
                                    })
                                    if (!res.ok) { alert('生成に失敗しました: ' + res.status); return }
                                    const blob = await res.blob()
                                    const url = URL.createObjectURL(blob)
                                    const a = document.createElement('a')
                                    a.href = url
                                    a.download = `ヒアリングシート_${it.client_name || ''}.xlsx`
                                    document.body.appendChild(a); a.click(); a.remove()
                                    URL.revokeObjectURL(url)
                                  } catch (e) {
                                    alert('生成に失敗しました: ' + e)
                                  }
                                }}
                                className="flex items-center gap-1.5 px-3 py-1.5 bg-emerald-700 hover:bg-emerald-600 text-white text-xs rounded-lg font-bold transition-colors"
                                title="必要なシートだけのExcelをその場で作ってダウンロードします（Gemini不要）"
                              >
                                📥 Excelで作成（{hearingSheets.length}枚）
                              </button>"""
s = s.replace(OLD, NEW, 1)
io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
