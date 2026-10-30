# -*- coding: utf-8 -*-
import urllib.request, json
from datetime import datetime, timezone

req = urllib.request.Request(
    'http://localhost:3001/api/delivery/items',
    headers={'Accept': 'application/json'}
)
with urllib.request.urlopen(req) as r:
    data = json.loads(r.read())

items = data.get('items', [])
print(f'Total items: {len(items)}')

# 14日以内・active のものを列挙
now = datetime.now(timezone.utc)
alert_items = []
for i in items:
    if i.get('status') == 'done':
        continue
    due_str = i.get('delivery_due_date', '')
    if not due_str:
        continue
    due = datetime.fromisoformat(due_str + 'T00:00:00+00:00')
    diff = (due - now).days
    if diff <= 14:
        alert_items.append({
            'client': i.get('client_name', ''),
            'status': i.get('status'),
            'due': due_str,
            'diff': diff,
            'missing': i.get('missing_in_last_import')
        })

print(f'\n14日以内 active件数: {len(alert_items)}')
for a in sorted(alert_items, key=lambda x: x['diff']):
    print(f"  {a['diff']:+d}日 | {a['client'][:20]} | missing={a['missing']}")
