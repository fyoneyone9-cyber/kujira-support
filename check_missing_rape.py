import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 中学・小学・幼女 通常レイプを全形式で探す
targets = ['char_rape_chuugaku', 'char_rape_shougaku', 'char_rape_youjo']
for t in targets:
    idx = content.find(t)
    if idx >= 0:
        print(f'{t}: pos={idx}')
        print(content[idx-30:idx+200])
        print()
    else:
        print(f'{t}: NOT FOUND')

# JD の outfits_ref を確認
print('\n=== JD outfits_ref確認 ===')
for cid in ['char_rape_jk_A', 'char_rape_jd_A', 'char_pov_rape_jd_A']:
    idx = content.find(f"'{cid}'")
    if idx < 0:
        idx = content.find(f'"{cid}"')
    if idx < 0:
        print(f'{cid}: NOT FOUND')
        continue
    chunk = content[idx:idx+500]
    ref_m = re.search(r'outfits_ref:\s*["\']([^"\']+)["\']', chunk)
    oc = len(re.findall(r'"label"', chunk))
    print(f'{cid}: ref={ref_m.group(1) if ref_m else "NONE"} inline_outfits={oc}')
    print(f'  {chunk[:300]}')
    print()
