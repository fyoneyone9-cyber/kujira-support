import urllib.request, json
r = urllib.request.urlopen('http://127.0.0.1:3002/api/version')
print(json.loads(r.read()))
