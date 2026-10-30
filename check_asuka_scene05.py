import sys, re, json
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# char_kaizou_med_asuka を含むpush()ブロックを抽出
m = re.search(r"window\.CHAR_TEMPLATES\.female\.push\(\{[^}]*'char_kaizou_med_asuka'[^}]*\}\);", content, re.DOTALL)
if not m:
    # id形式で再検索
    idx = content.find("'char_kaizou_med_asuka'")
    if idx < 0:
        idx = content.find('"char_kaizou_med_asuka"')
    if idx > 0:
        start = content.rfind('window.CHAR_TEMPLATES', 0, idx)
        end = content.find('});', idx) + 3
        block = content[start:end]
        # outfitsだけ抽出
        om = re.search(r"'outfits'\s*:\s*(\[.+?\])", block, re.DOTALL)
        if not om:
            om = re.search(r'"outfits"\s*:\s*(\[.+?\])', block, re.DOTALL)
        if om:
            try:
                outfits = json.loads(om.group(1))
                for i, o in enumerate(outfits):
                    print(f"[{i:02d}] {o.get('label','')[:60]}")
                    print(f"     {o.get('value','')[:100]}")
            except:
                print(om.group(1)[:500])
        else:
            print(block[:800])
    else:
        print("char_kaizou_med_asuka not found")
