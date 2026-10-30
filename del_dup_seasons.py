# -*- coding: utf-8 -*-
# DEL_DUP_SEASONS_V1: 完全使い回し6系列のS2〜S10キャラ＋グループ定義を削除（S1は残す）
import io, re, sys, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

P = r'C:\AI\ComfyUI\dashboard.html'
t = io.open(P, encoding='utf-8').read()
bak = P + '.bak_delseason_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
shutil.copy2(P, bak)
print('backup:', bak)

BASES = ['sennou', 'amaama', 'jk', 'ntrzuma', 'saimin', 'tentacle']
SEASONS = [str(n) for n in range(2, 11)]
id_re = re.compile(r"id:\s*'(char_(?:%s)_s(?:%s)_[a-z0-9_]+)'" % ('|'.join(BASES), '|'.join(SEASONS)))

def find_obj_bounds(text, id_pos):
    # id: の直前の '{' を探す
    s = text.rfind('{', 0, id_pos)
    # brace matching forward（文字列リテラル内の{}を考慮: '…' と "…" をスキップ）
    i = s; depth = 0; n = len(text)
    while i < n:
        c = text[i]
        if c in ("'", '"'):
            q = c; i += 1
            while i < n and text[i] != q:
                if text[i] == '\\': i += 1
                i += 1
        elif c == '{': depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0: return s, i+1
        i += 1
    return None

removed_chars = 0
while True:
    m = id_re.search(t)
    if not m: break
    b = find_obj_bounds(t, m.start())
    if not b:
        print('!! bounds fail at', m.group(1)); break
    s, e = b
    # push形式か確認: 前方に .push( があれば文全体を削除
    pre = t[max(0, s-80):s]
    pm = re.search(r'(window\.CHAR_TEMPLATES\.\w+\.push\(\s*)$', pre)
    if pm:
        s2 = s - len(pm.group(1))
        # 後ろの ); を含める
        e2 = e
        tail = t[e:e+10]
        tm = re.match(r'\s*\)\s*;?', tail)
        if tm: e2 = e + tm.end()
        t = t[:s2] + t[e2:]
    else:
        # 配列要素: 後続のカンマ、なければ前のカンマを除去
        e2 = e
        tail = t[e:e+5]
        tm = re.match(r'\s*,', tail)
        if tm:
            e2 = e + tm.end()
            t = t[:s] + t[e2:]
        else:
            s2 = s
            prem = re.search(r',\s*$', t[max(0,s-20):s])
            if prem: s2 = s - (len(t[max(0,s-20):s]) - prem.start())
            t = t[:s2] + t[e2:]
    removed_chars += 1
print('removed chars:', removed_chars)

# グループ定義エントリ削除: {key:'sennou_s2',...} 等（CHAR_GROUP_DEFS / CHAR_CATEGORIES 共通で単純オブジェクト）
gkeys = ['%s_s%s' % (b, s) for b in BASES for s in SEASONS]
removed_defs = 0
for gk in gkeys:
    # オブジェクトエントリ（fn/matchは1行の単純形）
    pat = re.compile(r"\{\s*key:\s*'%s'\s*,[^{}]*\}\s*,?" % re.escape(gk))
    t, n = pat.subn('', t)
    removed_defs += n
    # CHAR_CATEGORY_GROUPS cats配列内の 'key' トークン
    pat2 = re.compile(r"'%s'\s*,?" % re.escape(gk))
    # cats配列限定にするのは困難だが、グループ定義は上で消したので残る'キー'文字列はcats内のみのはず
    t, n2 = pat2.subn('', t)

print('removed group-def entries:', removed_defs)

# version +1
m = re.search(r'name="version" content="(\d+)"', t)
if m:
    ov = m.group(1); nv = str(int(ov)+1)
    t = t.replace('content="'+ov+'"', 'content="'+nv+'"')
    print('version:', ov, '->', nv)

io.open(P, 'w', encoding='utf-8').write(t)

# 残存チェック
left = id_re.findall(t)
print('leftover target ids:', len(left))
print('done')
