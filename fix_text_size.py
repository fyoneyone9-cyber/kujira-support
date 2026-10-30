import re, os

pages = ['keybox','paycube','p400-orders','ai-summary','purchase-orders','assignment','mail-templates','nippou','troubleshooting','admin','dashboard']
base = r'C:\GensparkClaw\kujira-support\src\app\(app)'

def upgrade_text_in_classname(content):
    # className属性の値だけを対象に処理する
    # rounded-fullを含む塊(バッジ系)は text-xs/sm をそのまま保持
    def replacer(m):
        cls = m.group(1)
        # バッジ系（rounded-fullと同居）はスキップ
        if 'rounded-full' in cls:
            return m.group(0)
        cls = cls.replace('text-xs', '\x00xs\x00').replace('text-sm', '\x00sm\x00')
        cls = cls.replace('\x00xs\x00', 'text-sm').replace('\x00sm\x00', 'text-base')
        return m.group(0)[0] + cls + m.group(0)[-1]

    # className="..." または className={`...`} や className={'...'}
    result = re.sub(r'className=("([^"]*)")', lambda m: 'className="' + (m.group(2) if 'rounded-full' in m.group(2) else m.group(2).replace('text-xs','text-sm').replace('text-sm','text-base').replace('text-sm','text-base')) + '"', content)
    return result

def process_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    changed = False
    
    for line in lines:
        new_line = line
        # className属性を含む行を処理
        # rounded-fullを含む行はバッジ系なのでスキップ
        if 'className=' in line and 'rounded-full' not in line:
            # text-xs -> text-sm, text-sm -> text-base
            # ただし既にtext-baseやtext-lgがある行の text-sm は慎重に
            tmp = new_line
            tmp = tmp.replace('text-xs', '\x00SM\x00')
            tmp = tmp.replace('text-sm', '\x00BASE\x00')
            tmp = tmp.replace('\x00SM\x00', 'text-sm')
            tmp = tmp.replace('\x00BASE\x00', 'text-base')
            new_line = tmp
        if new_line != line:
            changed = True
        new_lines.append(new_line)
    
    return '\n'.join(new_lines), changed

for page in pages:
    path = os.path.join(base, page, 'page.tsx')
    if not os.path.exists(path):
        print(f'Skip (not found): {page}')
        continue
    updated, changed = process_file(path)
    if changed:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(updated)
        print(f'Updated: {page}')
    else:
        print(f'No change: {page}')

print('Done.')
