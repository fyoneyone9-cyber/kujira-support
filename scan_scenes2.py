# scenes:[ の所属オブジェクトを特定する
import re, io
p = r'C:\AI\ComfyUI\dashboard.html'
s = io.open(p, 'r', encoding='utf-8').read()
for m in re.finditer(r'scenes\s*:\s*\[', s):
    st = m.start()
    ctx = s[max(0, st-3000):st]
    # find nearest preceding "key:'...'" or id
    ids = re.findall(r"(?:key|id)\s*:\s*'([^']+)'", ctx)
    print('scenes at', st, 'nearest ids:', ids[-3:])
# find the genre list structure: maybe "GENRE_DEFS" or similar with scenes
for pat in ['GENRES', 'genreDefs', 'STORY_GENRES', 'storyGenres', 'GENRE_DEFS', 'TK_GENRES']:
    ms = [m.start() for m in re.finditer(pat, s)]
    print(pat, len(ms), ms[:5])
# dump 1200 chars before first scenes
m = next(re.finditer(r'scenes\s*:\s*\[', s))
print(s[m.start()-2500:m.start()+100])
