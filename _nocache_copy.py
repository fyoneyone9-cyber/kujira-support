# -*- coding: utf-8 -*-
"""[GAS_NOCACHE_V1 2026-10-29] コピー時にキャッシュを確実に回避する。

症状: 配信ファイルからフロントチェックインは消えているのに、
      ダイアログには出続ける。
原因: コピーボタンの fetch がブラウザキャッシュから古い内容を取っていた。

対策:
  ・fetch に cache:'no-store' とタイムスタンプを付ける
  ・コピーした内容の先頭を検証し、古い版ならアラートで知らせる
  ・コピー完了時に「何バイトコピーしたか」を出して確認できるようにする
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_nocache_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

OLD1 = """                                                  try {
                                                    const r = await fetch('/api/delivery/gas-source?f=code')
                                                    await navigator.clipboard.writeText(await r.text())
                                                    alert('✅ コード.gs をコピーしました\\n\\nApps Scriptの「コード.gs」を全選択(Ctrl+A)して削除してから貼り付けてください')
                                                  } catch { alert('コピー失敗') }"""
assert s.count(OLD1) == 1, "anchor1: %d" % s.count(OLD1)
NEW1 = """                                                  try {
                                                    // [GAS_NOCACHE_V1] キャッシュから古い版を拾う事故を防ぐ
                                                    const r = await fetch('/api/delivery/gas-source?f=code&t=' + Date.now(),
                                                      { cache: 'no-store' })
                                                    const txt = await r.text()
                                                    if (!txt.includes('getSheetNames')) {
                                                      alert('⚠ 取得したコードが古い可能性があります。ページを Ctrl+Shift+R で再読込してください')
                                                      return
                                                    }
                                                    await navigator.clipboard.writeText(txt)
                                                    alert(`✅ コード.gs をコピーしました（${txt.length.toLocaleString()}文字）\\n\\n` +
                                                      'Apps Scriptの「コード.gs」を全選択(Ctrl+A)して削除してから貼り付けてください')
                                                  } catch { alert('コピー失敗') }"""
s = s.replace(OLD1, NEW1, 1)

OLD2 = """                                                  try {
                                                    const r = await fetch('/api/delivery/gas-source?f=dialog')
                                                    await navigator.clipboard.writeText(await r.text())
                                                    alert('✅ dialog.html をコピーしました\\n\\n作成した dialog ファイルの中身を全部消してから貼り付けてください')
                                                  } catch { alert('コピー失敗') }"""
assert s.count(OLD2) == 1, "anchor2: %d" % s.count(OLD2)
NEW2 = """                                                  try {
                                                    const r = await fetch('/api/delivery/gas-source?f=dialog&t=' + Date.now(),
                                                      { cache: 'no-store' })
                                                    const txt = await r.text()
                                                    // 古い版には固定チェックボックスがある。混入していたら警告する。
                                                    if (txt.includes('chk_pms') || !txt.includes('getSheetNames')) {
                                                      alert('⚠ 取得したHTMLが古い可能性があります。ページを Ctrl+Shift+R で再読込してください')
                                                      return
                                                    }
                                                    await navigator.clipboard.writeText(txt)
                                                    alert(`✅ dialog をコピーしました（${txt.length.toLocaleString()}文字）\\n\\n` +
                                                      'Apps Scriptの dialog を全選択(Ctrl+A)して削除してから貼り付けてください')
                                                  } catch { alert('コピー失敗') }"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
