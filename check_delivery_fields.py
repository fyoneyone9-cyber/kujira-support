import urllib.request, json
r = urllib.request.urlopen('http://localhost:3001/api/delivery/items?mode=all&limit=2')
d = json.loads(r.read())
items = d.get('items', [])
if items:
    print('Fields:', list(items[0].keys()))
    print(json.dumps(items[0], ensure_ascii=False, indent=2)[:800])
