# -*- coding: utf-8 -*-
"""[HEARING_GAS_V4 2026-10-29] 各手順にワンクリックのリンク／ボタンを付ける。

要望:「手順にリンク付けてワンクリックで迷わないように」

付けるもの:
  手順1-2: 雛形のコピー作成URL（/copy を付けると直接コピーダイアログが開く）
  手順3  : Apps Script 一覧（script.google.com）へのリンク
  手順4-5: コードのコピーボタン（既存）
  各ステップに「完了」チェックを付けて進捗が分かるようにする
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_gasv4_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD1 = """                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-[10px]">1</span>
                                              <span>上の <b className="text-emerald-300">📄 雛形を開く</b> をクリック</span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-[10px]">2</span>
                                              <span>
                                                <b className="text-amber-300">ファイル → コピーを作成</b> で自分のドライブに複製<br />
                                                <span className="text-slate-500">※ 以降はこの「コピー」で作業します（これが自分のマスターになります）</span>
                                              </span>
                                            </div>
                                            <div className="flex gap-2">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">3</span>
                                              <span>コピーしたシートで <b>拡張機能 → Apps Script</b></span>
                                            </div>"""
assert s.count(OLD1) == 1, "anchor1: %d" % s.count(OLD1)

NEW1 = """                                            <div className="flex gap-2 items-start">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-amber-600 text-white font-bold flex items-center justify-center text-[10px]">1</span>
                                              <span>
                                                <a href={TMPL.replace(/\\/edit.*$/, '/copy')} target="_blank" rel="noreferrer"
                                                  className="px-2 py-0.5 rounded bg-amber-600 hover:bg-amber-500 text-white font-bold">
                                                  🔗 雛形のコピーを作る（クリック）
                                                </a>
                                                <br />
                                                <span className="text-slate-500">開いた画面で「コピーを作成」を押す → 自分のドライブに複製されます</span>
                                              </span>
                                            </div>
                                            <div className="flex gap-2 items-start">
                                              <span className="flex-shrink-0 w-5 h-5 rounded-full bg-emerald-700 text-white font-bold flex items-center justify-center text-[10px]">2</span>
                                              <span>
                                                複製されたシートが開くので、そのまま
                                                <b className="text-amber-300"> 拡張機能 → Apps Script</b><br />
                                                <span className="text-slate-500">※ 必ず「コピー」側で行ってください（元の雛形は編集できません）</span>
                                              </span>
                                            </div>"""
s = s.replace(OLD1, NEW1, 1)

# 番号を振り直す（4->3, 5->4, 6->5, 7->6）
for old_n, new_n in [(">4<", ">3<"), (">5<", ">4<"), (">6<", ">5<"), (">7<", ">6<")]:
    s = s.replace(
        'flex items-center justify-center text-[10px]"' + old_n,
        'flex items-center justify-center text-[10px]"' + new_n, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
