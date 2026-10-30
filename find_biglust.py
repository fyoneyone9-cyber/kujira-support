import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\api_server_3001.py', encoding='utf-8', errors='replace') as f:
    for i, l in enumerate(f, 1):
        if 'biglust' in l.lower():
            print(i, l.rstrip())
