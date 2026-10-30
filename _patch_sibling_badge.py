# -*- coding: utf-8 -*-
"""[SIBLING_SYNC_V1] 同一現場が複数行あることを画面に出す。
黙って他の行を書き換えると「勝手に変わった」と混乱するため、
同期対象が存在する案件には件数バッジを表示する。"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_sibbadge_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

OLD = "                  {it.install_address && <p className=\"text-slate-400 text-sm\">\u8a2d\u7f6e\u5148: {it.install_address}"
i = s.index(OLD)
# 行末まで取得
eol = s.index("\n", i)
line = s[i:eol]
print("target line:", line[:160])

NEW = ("""                  {/* [SIBLING_SYNC_V1 2026-10-29] 同じ現場に複数案件がある場合の表示。
                      機材ステータス・発注日・入金状況はこれらの行で自動的に揃う。 */}
                  {siblingsOf(it).length > 0 && (
                    <p className="text-xs text-amber-300/90 mt-0.5">
                      🔗 同じ現場にあと{siblingsOf(it).length}件
                      <span className="text-amber-200/60 ml-1">（機材ステータス・発注日・入金状況は連動します）</span>
                    </p>
                  )}
""" + line)
s = s[:i] + NEW + s[eol:]

io.open(P, "w", encoding="utf-8").write(s)
print("badge added")
