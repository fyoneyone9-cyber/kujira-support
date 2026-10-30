# シーズン持ちジャンルのシーン格納場所を特定（例: aigan s1 vs s2 の outfits 比較）
import re, io, json
p = r'C:\AI\ComfyUI\dashboard.html'
s = io.open(p, 'r', encoding='utf-8').read()

def find_char(idpat):
    m = re.search(r"id:\s*'" + idpat + r"[^']*'", s)
    if not m:
        print('not found', idpat); return None
    st = m.start()
    # dump surrounding object ~ up to next "id:'" occurrence
    nxt = s.find("id:'", st + 10)
    chunk = s[st:nxt if nxt > 0 else st + 8000]
    return st, chunk

for pat in ['char_aigan_s1_', 'char_aigan_s2_', 'char_aigan_s5_']:
    r = find_char(pat)
    if r:
        st, chunk = r
        print('=' * 60)
        print(pat, 'at', st, 'len', len(chunk))
        print(chunk[:2500])
