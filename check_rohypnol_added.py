import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
ids = re.findall(r"id:'(char_rohypnol[^']*)'", content)
for x in sorted(set(ids)):
    print(x)
print('Total:', len(set(ids)))
