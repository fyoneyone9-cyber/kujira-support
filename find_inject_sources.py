import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

targets = [
    'tears on cheeks', 'tear streaks', 'wet cheeks from crying', 'teardrops falling',
    'glistening tears', 'red puffy eyes', 'watery eyes', 'tears streaming',
    'sweat:1', 'glistening skin', 'perspiring', 'wet skin from exertion', 'beads of sweat',
    'pink aroused skin tone', 'heat rising from skin', 'flushed skin', 'reddened chest',
    'eyes cast downward', 'avoiding eye contact',
    'stiff nipples', 'nipples hard',
]
for i, l in enumerate(lines, 1):
    lo = l.lower()
    for t in targets:
        if t in lo and ('inject' in lo or '+=' in l or 'text' in lo or '_add' in lo or '_pos' in lo):
            print(i, t[:25], '|', repr(l.rstrip()[:100]))
            break
