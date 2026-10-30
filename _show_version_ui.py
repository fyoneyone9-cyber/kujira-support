# -*- coding: utf-8 -*-
"""[GAS_VERSION_GUARD_V1] ダッシュボードにも最新バージョンを表示する。

「どれを貼れば正しいのか」が分からないのが事故の根。
コピーボタンの横に最新バージョンを出し、
ダイアログ側の表示と見比べられるようにする。
"""
import io, shutil, datetime, re

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_vershow_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

G = io.open(r"C:\GensparkClaw\kujira-support\public\docs\hearing-gas.js", encoding="utf-8").read()
ver = re.search(r"var GAS_VERSION = '([^']*)'", G).group(1)

OLD = """                                  <a href="/api/delivery/gas-source?f=code" target="_blank" rel="noreferrer\""""
assert s.count(OLD) == 1, "anchor"
NEW = """                                  {/* [GAS_VERSION_GUARD_V1 2026-10-29] 配信中のバージョンを表示。
                                      ダイアログ側の表示と一致しなければ貼り替えが必要。 */}
                                  <span className="text-sm px-2 py-1 rounded bg-slate-800 border border-slate-600 text-slate-300 font-mono">
                                    最新: %s
                                  </span>
                                  <a href="/api/delivery/gas-source?f=code" target="_blank" rel="noreferrer\"""" % ver
s = s.replace(OLD, NEW, 1)

# 手順にも「両方貼る」を強調
OLD2 = """                                              <span>
                                                <b>コード.gs</b>（既定で開いている）の中身を<b>全部消して</b>貼り付け"""
if s.count(OLD2) == 1:
    NEW2 = """                                              <span>
                                                <b className="text-rose-300">⚠ コード.gs と dialog は必ず両方セットで貼り替えてください</b>
                                                （片方だけだと動きません）<br />
                                                <b>コード.gs</b>（既定で開いている）の中身を<b>全部消して</b>貼り付け"""
    s = s.replace(OLD2, NEW2, 1)
    print("  手順に『両方セット』の注意を追加")

io.open(P, "w", encoding="utf-8").write(s)
print("ダッシュボードにバージョン表示を追加:", ver)
