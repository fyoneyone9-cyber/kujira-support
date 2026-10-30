import re

path = r'C:\GensparkClaw\kujira-support\src\app\(app)\delivery\page.tsx'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# type AlertLevel の直後（const LEAD_TIME_DAYS の前）にJITBOXヘルパーを挿入
jitbox_code = """
// JITBOXチャーター便の検出と大阪発リードタイム計算
function hasJitbox(it: { notes?: string; product_name?: string }): boolean {
  const text = `${it.notes || ''} ${it.product_name || ''}`.toLowerCase()
  return /jitbox|jitボックス|jit ボックス/.test(text)
}

function getJitboxLeadDays(installAddress: string): { days: number; note: string } {
  const addr = installAddress || ''
  if (/北海道|青森|岩手|秋田|沖縄|離島/.test(addr)) {
    return { days: 2, note: '大阪→当地 約900km超のため翌々日（日祝またぎは+1日）' }
  }
  if (/宮城|山形|福島/.test(addr)) {
    return { days: 2, note: '大阪→東北 約900km前後のため翌々日' }
  }
  return { days: 1, note: '大阪→当地 900km圏内のため翌日（目安）' }
}

"""

# const LEAD_TIME_DAYS の直前に挿入
target = 'const LEAD_TIME_DAYS'
if target in content:
    content = content.replace(target, jitbox_code + target, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('Inserted JITBOX helpers OK')
else:
    print('ERROR: target not found')
