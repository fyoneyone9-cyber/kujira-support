"""
覚醒剤S3 FF7キャラ(aerith/tifa)のoutfit valueをキャラ固有外見に修正。
jk_Aからコピーした「黒髪158cm制服16歳JK」タグをFF7キャラ固有に差し替え。
"""
import re, sys, io, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
shutil.copy2(path, path + '.bak_s3ff_fix')

with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# JK共通タグ（差し替え対象）
JK_HEAD = r'\(solo:2\.2\),\(1girl:2\.2\),\(only one person:2\.0\),\(2girls:0\.0\),\(multiple girls:0\.0\),\(exactly one girl:1\.6\),\(teenage girl:1\.8\),\(young:1\.7\),\(slender:1\.6\),\(small breasts:1\.5\),\(jk:1\.6\),16 years old,158cm,black long straight hair,school uniform,'

# エアリス固有外見
AERITH_HEAD = '(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(Aerith Gainsborough:1.9),(Final Fantasy VII:1.8),(ff7:1.8),(young woman:1.6),(slender:1.5),(medium breasts:1.5),22 years old,long brown braided hair,pink ribbon,green eyes,pink dress,'

# ティファ固有外見
TIFA_HEAD = '(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(Tifa Lockhart:1.9),(Final Fantasy VII:1.8),(ff7:1.8),(young woman:1.6),(athletic body:1.5),(large breasts:1.6),20 years old,long black hair,red eyes,white tank top,black miniskirt,'

def fix_char(content, char_id, new_head):
    # そのキャラのブロックを特定して置換
    idx = content.find("'" + char_id + "'")
    if idx == -1: idx = content.find('"' + char_id + '"')
    if idx == -1:
        print(f'{char_id}: NOT FOUND')
        return content, 0
    
    # ブロック終端（次のwindow.CHAR_TEMPLATESまで）
    end = content.find('window.CHAR_TEMPLATES', idx+1)
    if end == -1: end = idx + 50000
    block = content[idx:end]
    
    # outfit valueの先頭JKタグを置換（全outfits対象）
    new_block = re.sub(
        r'(value\s*:\s*["\'])' + JK_HEAD,
        r'\g<1>' + new_head.replace('\\', '\\\\'),
        block
    )
    count = len(re.findall(JK_HEAD, block))
    
    if count == 0:
        print(f'{char_id}: JKタグ見つからず（既に修正済みか別形式）')
        return content, 0
    
    content = content[:idx] + new_block + content[idx+len(block):]
    print(f'{char_id}: {count}件修正')
    return content, count

content, n1 = fix_char(content, 'char_kakuseizai_s3_ff_aerith', AERITH_HEAD)
content, n2 = fix_char(content, 'char_kakuseizai_s3_ff_tifa', TIFA_HEAD)

if n1 + n2 > 0:
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'書き込み完了 (計{n1+n2}件)')
else:
    print('変更なし')
