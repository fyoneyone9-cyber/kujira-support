# -*- coding: utf-8 -*-
"""[HEARING_GAS_V6 2026-10-29] 「メニューのどこに出るか」を明記する。

指摘:「メニューに📋ヒアリングシートあったけど分かりづらい、説明にないじゃん」
  手順6で「F5で再読み込み」とだけ書いており、
  ・メニューバーのどの位置に出るのか
  ・そこから何を選ぶのか
  を書いていなかった。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_menudesc_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = """                                              <span>コピーしたスプレッドシートのタブに戻り <b>F5 で再読み込み</b></span>"""
assert s.count(OLD) == 1, "anchor: %d" % s.count(OLD)
NEW = """                                              <span>
                                                コピーしたスプレッドシートのタブに戻り <b>F5 で再読み込み</b><br />
                                                <span className="text-slate-400">
                                                  メニューバーの <b className="text-amber-300">ヘルプ</b> の右隣に
                                                  <b className="text-amber-300"> 📋 ヒアリングシート</b> が追加されます<br />
                                                  <span className="text-slate-500">
                                                    （ファイル / 編集 / 表示 / 挿入 / 表示形式 / データ / ツール / 拡張機能 / ヘルプ / <b className="text-amber-300">📋 ヒアリングシート</b>）
                                                  </span>
                                                </span>
                                              </span>"""
s = s.replace(OLD, NEW, 1)

OLD2 = """                                            <p className="text-sm text-slate-300 leading-relaxed">
                                              雛形のメニュー <b className="text-amber-300">📋 ヒアリングシート</b> →
                                              <b>「必要シートだけコピー作成」</b><br />
                                              会社名・機材にチェック → <b>コピーを作成</b> → 新しいシートのリンクが出ます
                                            </p>"""
assert s.count(OLD2) == 1, "anchor2: %d" % s.count(OLD2)
NEW2 = """                                            <div className="text-sm text-slate-300 leading-relaxed space-y-1">
                                              <p>
                                                ① コピーしたシートのメニュー
                                                <b className="text-amber-300"> 📋 ヒアリングシート</b>（ヘルプの右隣）をクリック
                                              </p>
                                              <p>② <b>「必要シートだけコピー作成」</b> を選択</p>
                                              <p>③ 会社名・物件名・担当者・電話を入力し、導入機材にチェック</p>
                                              <p>④ <b className="text-emerald-300">コピーを作成</b> を押す</p>
                                              <p>
                                                ⑤ <b>▶ 作成したスプレッドシートを開く</b> のリンクが出るのでクリック<br />
                                                <span className="text-slate-500">保存先: マイドライブ直下 / ファイル名「ヒアリングシート_会社名_日付」</span>
                                              </p>
                                              <p className="text-amber-200 pt-1">
                                                ⚠ Apps Scriptのエディタ側で「実行」を押しても何も出ません。<br />
                                                必ず<b>スプレッドシートのメニューから</b>実行してください。
                                              </p>
                                            </div>"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
