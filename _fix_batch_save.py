# -*- coding: utf-8 -*-
"""[APPLICATION_IMPORT_V4 2026-10-29] 取り込んだ項目が1つしか保存されない問題を修正。

症状: 申込書を取り込んでも app_equips と app_imported_at しか残らない。

真因: saveTodoKey(id, currentTodos, key, val) は
      **引数で渡された currentTodos** に1キー足して丸ごと PATCH する。
      ループで連続呼び出しすると、毎回「取り込み前の todos」を基準にするため、
      後の呼び出しが前の結果を上書きして消してしまう（last-write-wins）。

対策: 複数キーを一度に保存する saveTodoBulk を新設し、
      申込書の取り込みはこれを使う。PATCH も1回で済む。
"""
import io, shutil, datetime

P = r"C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx"
shutil.copy2(P, P + ".bak_bulk_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
s = io.open(P, encoding="utf-8").read()

# saveTodoKey の直前に saveTodoBulk を追加
ANCHOR = "  const saveTodoKey = async (id: string,"
assert s.count(ANCHOR) == 1, "anchor1"
NEW = """  /**
   * [APPLICATION_IMPORT_V4 2026-10-29] 複数キーをまとめて保存する。
   * saveTodoKey を連続で呼ぶと、各呼び出しが「呼ばれた時点の todos」を基準に
   * 丸ごと PATCH するため、後の書き込みが前の結果を消してしまう。
   * 申込書の取り込みのように一度に何項目も入れる場合は必ずこちらを使うこと。
   */
  const saveTodoBulk = async (id: string, currentTodos: Record<string, unknown> | null | undefined,
                              patch: Record<string, string>) => {
    if (items.find(it => it.id === id)?.locked) {
      alert('🔒 この案件はロック中です。編集するにはロックを解除してください')
      return false
    }
    const todos: Record<string, unknown> = { ...(currentTodos || {}) }
    for (const [k, v] of Object.entries(patch)) todos[k] = v || null
    setItems(prev => prev.map(it => it.id === id ? { ...it, dashboard_todos: todos } : it))
    const res = await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id, dashboard_todos: todos })
    })
    return res.ok
  }

  const saveTodoKey = async (id: string,"""
s = s.replace(ANCHOR, NEW, 1)

# 申込書の取り込みを bulk に置き換え
OLD2 = """                                    patch['app_imported_at'] = new Date().toISOString().slice(0, 16).replace('T', ' ')
                                    for (const [k, v] of Object.entries(patch)) {
                                      await saveTodoKey(it.id, it.dashboard_todos, k, v)
                                    }"""
assert s.count(OLD2) == 1, "anchor2"
NEW2 = """                                    patch['app_imported_at'] = new Date().toISOString().slice(0, 16).replace('T', ' ')
                                    // [V4] 1キーずつ保存すると前の結果が消えるので、まとめて1回で保存する
                                    const ok = await saveTodoBulk(it.id, it.dashboard_todos, patch)
                                    if (!ok) { alert('保存に失敗しました'); return }"""
s = s.replace(OLD2, NEW2, 1)

io.open(P, "w", encoding="utf-8").write(s)
print("patched OK")
