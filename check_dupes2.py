import sys, urllib.request, json
sys.stdout.reconfigure(encoding='utf-8')

url = 'https://fjkpdejyusnttbhdmyxt.supabase.co/rest/v1/delivery_items?select=id,client_name,install_address,product_name,item_key,status&client_name=eq.%E6%A0%AA%E5%BC%8F%E4%BC%9A%E7%A4%BE%E3%83%9B%E3%83%86%E3%83%AB%E3%82%A8%E3%83%BC%E3%82%B9&limit=20'
req = urllib.request.Request(url, headers={
    'apikey': 'sb_publishable_BBN8pHofRc1V3NWKoi81xg_hXZkH3dp',
    'Authorization': 'Bearer sb_publishable_BBN8pHofRc1V3NWKoi81xg_hXZkH3dp'
})
data = json.loads(urllib.request.urlopen(req).read())
print(f'件数: {len(data)}')
for r in data:
    print(f"ID={r['id']}")
    print(f"  client:  [{r['client_name']}]")
    print(f"  address: [{r['install_address']}]")
    print(f"  product: [{r['product_name']}]")
    print(f"  key:     [{r['item_key']}]")
    print(f"  status:  {r['status']}")
    print()
