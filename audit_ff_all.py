"""今日追加したFF7キャラ全件のoutfit value先頭を確認"""
import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

FF7_CHARS = [
    'char_kakuseizai_s3_ff_aerith',
    'char_kakuseizai_s3_ff_tifa',
    'char_rape_ff_aerith',
    'char_rape_ff_tifa',
    'char_rape30_ff_aerith',
    'char_rape30_ff_tifa',
    'char_rohypnol_aerith',
    'char_rohypnol_tifa',
    'char_rohypnol_s2_aerith',
    'char_rohypnol_s2_tifa',
]

AERITH_KWS = ['aerith','gainsborough','brown braided','pink ribbon','pink dress']
TIFA_KWS   = ['tifa','lockhart','long black hair','white tank top','black miniskirt']

for tid in FF7_CHARS:
    idx = content.find("'" + tid + "'")
    if idx == -1: idx = content.find('"' + tid + '"')
    if idx == -1:
        print(f'[NOT FOUND] {tid}')
        continue

    end = content.find('window.CHAR_TEMPLATES', idx+1)
    if end == -1: end = idx + 50000
    block = content[idx:end]

    # 全outfit valueを取得
    values = re.findall(r'value\s*:\s*["\']([^"\']{0,300})', block)
    if not values:
        print(f'[NO OUTFITS] {tid}')
        continue

    kws = AERITH_KWS if 'aerith' in tid else TIFA_KWS
    bad = [v for v in values if not any(k in v.lower() for k in kws)]
    ok  = len(values) - len(bad)

    if bad:
        print(f'[NG] {tid}: {ok}OK / {len(bad)}NG')
        print(f'     NG例: {bad[0][:120]}')
    else:
        print(f'[OK] {tid}: 全{len(values)}件 キャラタグあり')
