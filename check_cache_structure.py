import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if any(k in l for k in ['_panel_meta_cache', '_pages_cache', '_char_cache', 'char_id.*cache', 'cache.*char_id']):
        if any(k in l for k in ['def ', '= {}', '= dict', 'clear()', 'del ', 'pop(']):
            print(f'L{i+1}: {l.rstrip()}')
