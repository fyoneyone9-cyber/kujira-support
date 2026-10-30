# 調査: tifa/aerith キャラのid・シーン(scenes)・outfits構造を確認
import re, io, json

p = r'C:\AI\ComfyUI\dashboard.html'
s = io.open(p, 'r', encoding='utf-8').read()

ids = sorted(set(re.findall(r"id:\s*'([^']*(?:tifa|aerith)[^']*)'", s)))
print("IDS:", len(ids))
for i in ids:
    print(" ", i)

# 各キャラのpushブロック位置と、scenes/outfitsの個数を確認
for cid in ids:
    for m in re.finditer(re.escape("id: '" + cid + "'"), s):
        start = m.start()
        # push( の開始を遡る
        # ブロック終端: 対応する push({...}); を大まかに切り出し（次のpushまたは5000字）
        chunk = s[start:start+40000]
        scenes = re.findall(r"label:\s*'([^']*)'\s*,\s*value:\s*'", chunk[:40000])
        print("=" * 60)
        print(cid, "at", start)
        # outfits数
        om = re.search(r"outfits\s*:\s*\[", chunk)
        print(" outfits_pos:", om.start() if om else None)
        # scenesキー有無
        sm = re.search(r"scenes\s*:\s*\[", chunk)
        print(" scenes_pos:", sm.start() if sm else None)
        break
