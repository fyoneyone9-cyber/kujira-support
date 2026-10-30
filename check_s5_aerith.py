import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
m = re.search(r'id:\s*[\'"]char_kaizo_nichijou5_aerith[\'"][^\}]{0,300}', content)
if m:
    print(m.group()[:300])
