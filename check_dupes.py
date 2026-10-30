import sys, urllib.request, json
from collections import Counter
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://fjkpdejyusnttbhdmyxt.supabase.co/rest/v1/delivery_items?select=id,client_name,install_address,product_name,item_key,status,created_at&order=client_name&limit=1000'
req = urllib.request.Request(url, headers={
    'apikey': 'sb_publishable_BBN8pHofRc1V3NWKoi81xg_hXZkH3dp',
    'Authorization': 'Bearer sb_publishable_BBN8pHofRc1V3NWKoi81xg_hXZkH3dp'
})
data = json.loads(urllib.request.urlopen(req).read())

keys = [d['item_key'] for d in data]
dupes = {k: v for k, v in Counter(keys).items() if v > 1}
print(f'総件数: {len(data)}')
print(f'重複item_keyの種類: {len(dupes)}')
print()
for k, cnt in list(dupes.items())[:10]:
    rows = [d for d in data if d['item_key'] == k]
    for r in rows:
        rid = r['id']
        name = r['client_name']
        prod = r['product_name']
        ca = r['created_at'][:16]
        st = r['status']
        print(f"  ID={rid} | {name} | {prod} | status={st} | created={ca}")
    print()
