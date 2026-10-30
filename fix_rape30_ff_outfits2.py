"""
char_rape30_ff_aerith/tifa のoutfit valueにキャラタグを先頭注入。
outfit valueは状況タグのみ（キャラ外見タグなし）→ 先頭にキャラ識別タグを追加。
"""
import re, sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
shutil.copy2(path, path + '.bak_rape30ff2')

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

AERITH_PREFIX = '(Aerith Gainsborough:1.9),(Final Fantasy VII:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(medium breasts:1.5),22 years old,long brown braided hair,pink ribbon,green eyes,'
TIFA_PREFIX   = '(Tifa Lockhart:1.9),(Final Fantasy VII:1.8),(ff7:1.8),(young woman:1.6),(athletic body:1.5),(large breasts:1.6),20 years old,long black hair,red eyes,'

def inject_prefix(content, char_id, prefix):
    idx = content.find("'" + char_id + "'")
    if idx == -1: idx = content.find('"' + char_id + '"')
    if idx == -1:
        print(f'{char_id}: NOT FOUND'); return content, 0

    end = content.find('window.CHAR_TEMPLATES', idx+1)
    if end == -1: end = idx + 50000
    block = content[idx:end]

    kws = ['aerith','gainsborough','tifa','lockhart','long black hair','brown braided','pink ribbon']

    def replacer(m):
        val = m.group(2)
        if any(k in val.lower() for k in kws):
            return m.group(0)  # 既にキャラタグあり → スキップ
        return m.group(1) + prefix + val

    new_block, count = re.subn(
        r'(value\s*:\s*["\'])([^"\']{10,})',
        replacer,
        block
    )
    content = content[:idx] + new_block + content[idx+len(block):]
    print(f'{char_id}: {count}件処理')
    return content, count

content, n1 = inject_prefix(content, 'char_rape30_ff_aerith', AERITH_PREFIX)
content, n2 = inject_prefix(content, 'char_rape30_ff_tifa', TIFA_PREFIX)

if n1 + n2 > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'書き込み完了 計{n1+n2}件')
