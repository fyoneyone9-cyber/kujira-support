import urllib.request, json
r = urllib.request.urlopen(urllib.request.Request(
    'http://localhost:3001/api/admin/rebuild',
    data=b'{}', method='POST',
    headers={'Content-Type': 'application/json'}
))
print('rebuild triggered:', r.status)
