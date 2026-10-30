import sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# /api/generate-panel へのfetch bodyを探す
for i, l in enumerate(lines, 1):
    if 'generate-panel' in l or ('outfit' in l.lower() and ('body:' in l or 'JSON.stringify' in l)):
        print(i, repr(l.rstrip()[:160]))
