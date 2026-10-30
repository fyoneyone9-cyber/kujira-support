import re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

tid = 'char_kakuseizai_s3_ff_aerith'
idx = content.find("'" + tid + "'")
if idx == -1: idx = content.find('"' + tid + '"')
# このキャラ定義ブロック全体（次のpush(まで）
end = content.find('window.CHAR_TEMPLATES', idx+1)
if end == -1: end = idx + 3000
chunk = content[idx:end]

# outfits_ref または outfits の先頭を確認
m_ref = re.search(r"outfits_ref\s*:\s*['\"]([^'\"]+)['\"]", chunk)
if m_ref:
    print('outfits_ref:', m_ref.group(1))
else:
    # outfitsの最初のエントリ
    m = re.search(r"outfits\s*:\s*\[.*?\{(.*?)\}", chunk, re.DOTALL)
    if m:
        print('first outfit entry:', m.group(1)[:300])
    else:
        print('outfits not found in chunk')
        print('chunk head:', chunk[:500])
