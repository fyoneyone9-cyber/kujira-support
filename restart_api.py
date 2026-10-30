import urllib.request, json
r = urllib.request.urlopen(urllib.request.Request(
    'http://127.0.0.1:3002/api/restart?force=1',
    data=b'{}', method='POST'
))
print(r.read())
