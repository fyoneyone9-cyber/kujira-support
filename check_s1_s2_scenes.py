import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

def get_outfits(prefix):
    idx = content.find(prefix)
    if idx < 0:
        return [], idx
    oi = content.find('outfits:', idx)
    if oi < 0 or oi - idx > 3000:
        return [], idx
    start = content.find('[', oi)
    if start < 0:
        return [], idx
    depth = 0
    end = start
    for i in range(start, min(start+300000, len(content))):
        if content[i] == '[': depth += 1
        elif content[i] == ']':
            depth -= 1
            if depth == 0:
                end = i+1
                break
    chunk = content[start:end]
    labels = re.findall(r"label:\s*['\"]([^'\"]+)['\"]", chunk)
    return labels, idx

# S1の実際の構造を確認（outfitsがどこに）
for prefix in ['char_kakuseizai_jk_A', 'char_kakuseizai_s2_jk_A']:
    idx = content.find(prefix)
    if idx < 0:
        print(f'{prefix}: NOT FOUND')
        continue
    chunk = content[idx:idx+500]
    print(f'{prefix}:')
    print(chunk[:300])
    print('...')
    print()
