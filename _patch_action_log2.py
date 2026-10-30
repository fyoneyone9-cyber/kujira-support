# -*- coding: utf-8 -*-
"""[INTEG_ACTION_LOG_V1] IntegRow の閉じ構造を直し、未連携のときだけ対応履歴欄を出す。"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_actionlog2_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                        {/* 正規ヒアリングシートURLが入力済みなら開くボタン */}
                        {it.hearing_sheet_url && (
                          <a href={it.hearing_sheet_url} target="_blank" rel="noreferrer"
                            className="ml-auto text-xs px-2 py-0.5 bg-blue-700 hover:bg-blue-600 border border-blue-500 text-blue-100 rounded whitespace-nowrap font-bold">
                            📄 ヒアリングシートを開く
                          </a>
                        )}
                      </div>
                    )
                  }"""
assert s.count(OLD) == 1, "anchor"

NEW = """                        {/* 正規ヒアリングシートURLが入力済みなら開くボタン */}
                        {it.hearing_sheet_url && (
                          <a href={it.hearing_sheet_url} target="_blank" rel="noreferrer"
                            className="ml-auto text-xs px-2 py-0.5 bg-blue-700 hover:bg-blue-600 border border-blue-500 text-blue-100 rounded whitespace-nowrap font-bold">
                            📄 ヒアリングシートを開く
                          </a>
                        )}
                      </div>
                      {/* [INTEG_ACTION_LOG_V1] 未連携(=要対応)のときだけ対応履歴欄を出す。
                          連携済み/不要になったら畳んで画面を汚さない。 */}
                      {val === null && <IntegActionLog field={field} />}
                      </div>
                    )
                  }"""
s = s.replace(OLD, NEW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
