import sys, urllib.request, json
sys.stdout.reconfigure(encoding='utf-8')

# まずアイテムを1件取得
r = urllib.request.urlopen('http://localhost:3001/api/delivery/items?mode=all&limit=5')
d = json.loads(r.read())
items = [i for i in d['items'] if i.get('status') != 'done']
if not items:
    print('activeなアイテムなし')
    sys.exit()

it = items[0]
print(f"テスト対象: {it['client_name']} id={it['id']}")
print(f"現在 jitbox_ordered={it.get('jitbox_ordered')} worker_needed={it.get('worker_needed')}")
print(f"現在 dashboard_todos={json.dumps(it.get('dashboard_todos'), ensure_ascii=False)}")

# PATCHを試す
payload = json.dumps({'id': it['id'], 'dashboard_todos': {**(it.get('dashboard_todos') or {}), '__test__': 'ok'}}).encode()
req = urllib.request.Request('http://localhost:3001/api/delivery/items', data=payload, method='PATCH',
    headers={'Content-Type': 'application/json'})
r2 = urllib.request.urlopen(req)
res = json.loads(r2.read())
print(f"\nPATCH response status: {r2.status}")
print(f"response: {json.dumps(res, ensure_ascii=False)[:300]}")

# 確認のため再取得
r3 = urllib.request.urlopen(f'http://localhost:3001/api/delivery/items?mode=all&limit=100')
d3 = json.loads(r3.read())
match = next((i for i in d3['items'] if i['id'] == it['id']), None)
if match:
    print(f"\n再取得後 dashboard_todos={json.dumps(match.get('dashboard_todos'), ensure_ascii=False)[:200]}")
    if match.get('dashboard_todos', {}).get('__test__') == 'ok':
        print('✅ DB保存成功')
    else:
        print('❌ DB保存失敗 - テストキーが反映されていない')
