# -*- coding: utf-8 -*-
path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 型定義に locked と jitbox_ordered を追加
old_type = '  worker_contacts?: { name: string; tel: string; email: string }[] | null\n}'
new_type = '  worker_contacts?: { name: string; tel: string; email: string }[] | null\n  locked?: boolean | null\n  jitbox_ordered?: boolean | null\n}'
if old_type in content:
    content = content.replace(old_type, new_type, 1)
    print('Type fields added OK')
else:
    print('ERROR: type not found')

# 2. toggleJitboxOrdered 関数を saveWorkDate の直前に追加
toggle_fn = '''
  const toggleJitboxOrdered = async (it: DeliveryItem) => {
    const next = !it.jitbox_ordered
    const msg = next
      ? `\u300c${it.client_name}\u300dのJITBOX手配を「手配済み」にしますか？`
      : `\u300c${it.client_name}\u300dのJITBOX手配を「未手配」に戻しますか？`
    if (!window.confirm(msg)) return
    setItems(prev => prev.map(p => p.id === it.id ? { ...p, jitbox_ordered: next } : p))
    await fetch('/api/delivery/items', {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: it.id, jitbox_ordered: next })
    })
  }

  const markDone'''

if '  const markDone' in content:
    content = content.replace('  const markDone', toggle_fn, 1)
    print('toggleJitboxOrdered inserted OK')
else:
    print('ERROR: markDone not found')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done.')
