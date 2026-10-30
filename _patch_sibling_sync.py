# -*- coding: utf-8 -*-
"""[SIBLING_SYNC_V1 2026-10-29] 同一現場(会社名+設置先住所)の複数行で、
現場共通の情報(入金状況・機材手配ステータス・発注日/到着予定日/実到着日)を自動で揃える。

背景(ユーザー指摘):「2個あるなら1つ目のステータスとか日付とか同期されてくれない?」
 - item_key は「会社名|設置先住所|製品名」で作られるため、同じホテルでも
   製品が違えば別行になる(実データで 321グループ中 60グループが複数行)。
 - 入金確認(payment_status)や P400 の発注日などは「現場単位で1つ」の情報なのに
   行ごとに独立しており、片方だけ入力されている状態が 8グループ存在した。
 - 特に payment_status は PayCube/キーボックスの発注ブロック条件なので、
   同じ現場なのに片方の行からは発注できない、という実害が出る。

対策: 共通項目を保存したとき、同一現場の兄弟行にも同じ値を書く。
      製品固有の情報(台数/製品名/納期/進捗)は対象外。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
bak = P + ".bak_siblingsync_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
shutil.copy2(P, bak)
print("backup:", bak)
s = io.open(P, encoding="utf-8").read()

# ---------------------------------------------------------------- 1) 同期ヘルパーを追加
OLD = """  const saveTodoKey = async (id: string, currentTodos: Record<string, unknown> | null | undefined, key: string, val: string) => {
    if (items.find(it => it.id === id)?.locked) { alert('\U0001f512 この案件はロック中です。編集するにはロックを解除してください。'); return }
    const todos = { ...(currentTodos || {}), [key]: val || null }
    // 楽観的更新（保存前にUIに即反映）
    setItems(prev => prev.map(it => it.id === id ? { ...it, dashboard_todos: todos } : it))
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, dashboard_todos: todos })
    })
  }"""
assert s.count(OLD) == 1, "saveTodoKey anchor"

NEW = """  // [SIBLING_SYNC_V1 2026-10-29] 同一現場(会社名+設置先住所)で共有すべき項目。
  //   item_keyが「会社名|住所|製品名」のため、同じホテルでも製品が違えば別行になる。
  //   入金確認や機材の発注日は「現場単位で1つ」の情報なので、行ごとにバラバラだと
  //   片方だけ入金未確認扱いになり PayCube/キーボックスの発注がブロックされる等の実害が出る。
  //   ⚠ 製品固有の情報(台数/製品名/納期/進捗/MTID等)はここに入れないこと。
  const SIBLING_SHARED_KEY = (k: string) =>
    /^manual_.*_status$/.test(k) ||          // P400/PayCube/VEGA3000 の手配状況
    /_order_date$/.test(k) ||                // 発注日
    /_arrive_date$/.test(k) ||               // 到着予定日
    /_actual_date$/.test(k) ||               // 実到着日
    k === 'keybox_status' || k === 'paypay_status' ||
    k === 'payment_status' || k === 'payment_memo'

  // 同じ現場(会社名+設置先住所)の他の行を返す
  const siblingsOf = (it: Item) =>
    items.filter(x => x.id !== it.id &&
      x.client_name === it.client_name &&
      (x.install_address || '') === (it.install_address || ''))

  const saveTodoKey = async (id: string, currentTodos: Record<string, unknown> | null | undefined, key: string, val: string) => {
    if (items.find(it => it.id === id)?.locked) { alert('\U0001f512 この案件はロック中です。編集するにはロックを解除してください。'); return }
    const todos = { ...(currentTodos || {}), [key]: val || null }
    // 楽観的更新（保存前にUIに即反映）
    setItems(prev => prev.map(it => it.id === id ? { ...it, dashboard_todos: todos } : it))
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, dashboard_todos: todos })
    })

    // [SIBLING_SYNC_V1] 現場共通の項目なら、同じ現場の他の行にも同じ値を反映する
    if (!SIBLING_SHARED_KEY(key)) return
    const me = items.find(x => x.id === id)
    if (!me) return
    const sibs = siblingsOf(me).filter(x => !x.locked)
    if (!sibs.length) return
    setItems(prev => prev.map(x => sibs.some(sx => sx.id === x.id)
      ? { ...x, dashboard_todos: { ...(x.dashboard_todos || {}), [key]: val || null } }
      : x))
    await Promise.all(sibs.map(sx => fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: sx.id, dashboard_todos: { ...(sx.dashboard_todos || {}), [key]: val || null } })
    }).catch(() => {})))
    console.info('[SIBLING_SYNC_V1] %s=%s を同一現場の%d件へ同期', key, val, sibs.length)
  }"""
s = s.replace(OLD, NEW, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("saveTodoKey patched")
