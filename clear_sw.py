import subprocess, time, urllib.request, json

# Chromeのデバッグポートに接続してService Workerをクリア
try:
    tabs = json.loads(urllib.request.urlopen('http://localhost:9222/json').read())
    delivery_tab = next((t for t in tabs if 'localhost:3001' in t.get('url','')), None)
    if delivery_tab:
        print('Found tab:', delivery_tab['url'])
    else:
        print('No localhost:3001 tab found')
        print('Tabs:', [t.get('url') for t in tabs])
except Exception as e:
    print('Chrome debug port not available:', e)
    print('Starting Chrome with debug port...')
    subprocess.Popen([
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        '--remote-debugging-port=9222',
        'http://localhost:3001/delivery'
    ])
    time.sleep(3)
    try:
        tabs = json.loads(urllib.request.urlopen('http://localhost:9222/json').read())
        print('Tabs:', [t.get('url') for t in tabs])
    except Exception as e2:
        print('Still failed:', e2)
