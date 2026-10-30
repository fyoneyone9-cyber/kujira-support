import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 医療改造キャラを全部抽出（block22あたりにある1行push形式）
# char_kaizo_med_ または char_kaizou_med_ を含むpush
pattern = re.compile(r'window\.CHAR_TEMPLATES\.female\.push\((\{.+?\})\);', re.DOTALL)
chars = pattern.finditer(content)
for m in chars:
    obj = m.group(1)
    if 'kaizo_med' not in obj and 'kaizou_med' not in obj:
        continue
    id_m = re.search(r"id:\s*['\"]([^'\"]+)['\"]", obj)
    ref_m = re.search(r"outfits_ref:\s*['\"]([^'\"]+)['\"]", obj)
    outfits_count = len(re.findall(r'"label":', obj))
    char_id = id_m.group(1) if id_m else '?'
    ref = ref_m.group(1) if ref_m else f'inline({outfits_count}scenes)' if outfits_count else 'NONE'
    print(char_id, '|', ref)
