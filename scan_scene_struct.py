# 目的: シーン定義構造（label+value のシーンリスト）とシーズン構造を特定
import re, collections
p = r'C:\AI\ComfyUI\dashboard.html'
s = open(p, encoding='utf-8', errors='ignore').read()

for kw in ['SCENE_PACK', 'GENRE_SCENES', 'scenePresets', 'SCENE_LIST', 'seasons', 'SEASON', 'season:', 'シーズン']:
    idxs = [m.start() for m in re.finditer(re.escape(kw), s)]
    print(kw, len(idxs), idxs[:10])
