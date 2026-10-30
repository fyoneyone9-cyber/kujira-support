import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

idx = content.find('char_rohypnol_aerith')
chunk = content[idx:idx+120000]

# outfit オブジェクト全体を抽出（label + value を同一オブジェクトから取る）
outfit_objs = re.findall(r'\{[^{}]{0,800}\}', chunk)
sex_labels = ['挿入①','挿入②','体位①','体位②','体位③','射精','事後①']
for i, obj in enumerate(outfit_objs):
    for sl in sex_labels:
        if sl in obj:
            has1boy = '1boy' in obj
            vm = re.search(r'"value"\s*:\s*"([^"]{0,400})"', obj)
            val = vm.group(1)[:250] if vm else '(no value)'
            print(f'[obj#{i}] {sl} | 1boy={has1boy}')
            print(f'  {val}')
            print()
            break
