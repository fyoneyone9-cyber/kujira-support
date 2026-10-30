# -*- coding: utf-8 -*-
import urllib.request, json

req = urllib.request.Request('http://localhost:3001/api/delivery/items',
    headers={'Accept': 'application/json'})
with urllib.request.urlopen(req) as r:
    d = json.loads(r.read())

items = [i for i in d['items'] if i.get('todos')]
for i in items[:5]:
    name = (i.get('client_name') or '')[:20]
    keys = list((i.get('todos') or {}).keys())[:10]
    print(repr(name), '->', keys)
