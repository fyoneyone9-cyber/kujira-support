import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

for cid in ["char_kakuseizai_s2_tifa", "char_kakuseizai_s2_aerith"]:
    idx = content.find(cid)
    if idx < 0:
        print(f"{cid}: NOT FOUND"); continue
    # 前後確認
    chunk = content[idx:idx+200]
    print(f"{cid}: {chunk[:150]}")
    # outfitsを文字列として取得
    oi = content.find("outfits:", idx)
    start = content.find('[', oi)
    chunk2 = content[start:start+500]
    # JSオブジェクト形式確認
    print(f"  outfits start: {chunk2[:200]}")
    print()
