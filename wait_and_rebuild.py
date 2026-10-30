import time, urllib.request, json

for i in range(15):
    try:
        r = urllib.request.urlopen('http://localhost:3001/api/delivery/items?mode=all&limit=1', timeout=3)
        if r.status == 200:
            print(f'Server up after {i*2}s')
            break
    except:
        print(f'waiting... {i*2}s')
        time.sleep(2)

r = urllib.request.urlopen(urllib.request.Request(
    'http://localhost:3001/api/admin/rebuild',
    data=b'{}', method='POST',
    headers={'Content-Type': 'application/json'}
))
print('rebuild triggered:', r.status)
