import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
# nichijou4 の登録箇所
for m in re.finditer(r'.{0,120}nichijou4.{0,120}', content):
    line = m.group()
    if 'registerGenre' in line or 'CHAR_GROUP' in line or 'CHAR_CATEG' in line or 'bigGenre' in line:
        print(repr(line[:200]))
