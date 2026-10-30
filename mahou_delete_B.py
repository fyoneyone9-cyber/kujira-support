# -*- coding: utf-8 -*-
# B案: 画像9グループ削除（苗床S1-10は残す）
# 対象キャラ:
#  - char_mahou_shoujo_* (12)         複数行push
#  - char_mahou_(youjo|shougaku|chuugaku|jk)_* (13)  複数行push
#  - char_mahou_youchien_* (5)        複数行push
#  - char_manga_mahou_* (21)          "id":"..." push（JSONキー形式）
#  - char_tentacle_(youjo|shougaku|chuugaku|elf|mahou|nurse)_* (24) 配列オブジェクト/push混在
# 方式: id出現位置から push( または オブジェクト開始 { を特定し、括弧対応で終端まで削除
import re, sys, io, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ts = time.strftime('%Y%m%d_%H%M%S')
DB = r'C:\AI\ComfyUI\dashboard.html'

db_bak = DB.replace('.html', f'_backup_{ts}_mahoudelB.html')
shutil.copy2(DB, db_bak)
print('backup:', db_bak)

s = open(DB, encoding='utf-8').read()
orig_len = len(s)

TARGET = re.compile(
    r"char_(?:"
    r"mahou_shoujo_[a-zA-Z0-9_]+"
    r"|mahou_(?:youjo|shougaku|chuugaku|jk)_[a-zA-Z0-9_]+"
    r"|mahou_youchien_[a-zA-Z0-9_]+"
    r"|manga_mahou_[a-zA-Z0-9_]+"
    r"|tentacle_(?:youjo|shougaku|chuugaku|elf|mahou|nurse)_[a-zA-Z0-9_]+"
    r")")

def find_obj_bounds(s, id_pos):
    """id_posを含むオブジェクトリテラルの { ... } 範囲を括弧対応で返す。
    さらに直前が push( なら push 呼び出し全体を範囲にする。"""
    # idキーの直前の { を探す（ネスト考慮: idは必ずオブジェクト直下第一階層付近）
    i = id_pos
    depth = 0
    start = -1
    while i > 0:
        c = s[i]
        if c == '}':
            depth += 1
        elif c == '{':
            if depth == 0:
                start = i
                break
            depth -= 1
        i -= 1
    assert start >= 0
    # 終端: 括弧対応（文字列内の{}は厳密でないがJS定義では稀。patterns内はバランスする）
    j = start
    depth = 0
    in_str = None
    esc = False
    while j < len(s):
        c = s[j]
        if esc:
            esc = False
        elif c == '\\':
            esc = True
        elif in_str:
            if c == in_str:
                in_str = None
        elif c in ('"', "'", '`'):
            in_str = c
        elif c == '{':
            depth += 1
        elif c == '}':
            depth -= 1
            if depth == 0:
                j += 1
                break
        j += 1
    end = j
    # push( ラッパー確認
    pre = s[max(0, start-80):start]
    m = re.search(r"(?:window\.)?CHAR_TEMPLATES\.female\.push\(\s*$", pre)
    if m:
        start = start - (len(pre) - m.start())
        # end: ); まで
        k = end
        while k < len(s) and s[k] in ' \n\r\t':
            k += 1
        if s[k:k+2] == ');':
            end = k + 2
    else:
        # 配列要素: 後続カンマを含める
        k = end
        while k < len(s) and s[k] in ' \n\r\t':
            k += 1
        if k < len(s) and s[k] == ',':
            end = k + 1
    # 末尾改行を1つ食う
    if end < len(s) and s[end] == '\n':
        end += 1
    return start, end

removed_ids = []
while True:
    m = re.search(r"[\"']id[\"']\s*:\s*[\"'](" + TARGET.pattern + r")[\"']|id:\s*[\"'](" + TARGET.pattern + r")[\"']", s)
    if not m:
        break
    cid = m.group(1) or m.group(2)
    st, en = find_obj_bounds(s, m.start())
    seg = s[st:en]
    # 安全確認: セグメントに別キャラのid定義が含まれないこと
    other = [x for x in re.findall(r"id[\"']?\s*:\s*[\"'](char_[a-zA-Z0-9_]+)[\"']", seg) if x != cid]
    assert not other, (cid, other[:3])
    s = s[:st] + s[st:en].__class__() + s[en:]
    removed_ids.append(cid)

print('chars removed:', len(removed_ids))
# 全削除IDがターゲットパターンに完全一致し、苗床S(char_tentacle_sN_)を含まないことを検証
for x in removed_ids:
    assert TARGET.fullmatch(x), x
    assert not re.match(r'char_tentacle_s\d+_', x), x
assert 70 <= len(removed_ids) <= 90, len(removed_ids)

# GD定義削除（各形式）
patterns = [
    # fn形式（bigGenre付き）
    r"\{key:'(?:magic_youjo|mahou|mahou_tentacle|tentacle_mahou|tentacle_elf|mahou_shoujo|mahou_youjo|mahou_youchien|manga_mahou|tentacle)',label:\"[^\"]*\",fn:id => [^\n]*?,bigGenre:'[^']*'\},\n*",
    # match形式
    r"\{\s*key:'(?:magic_youjo|mahou|mahou_tentacle|tentacle_mahou|tentacle_elf|mahou_shoujo|mahou_youjo|mahou_youchien|manga_mahou|tentacle|mahou_age|mahou_jk|mahou_shougaku|mahou_chuugaku|manga_mahou_jc|manga_mahou_jk)',\s*label:\s*[\"'][^\"']*[\"'],\s*match: id => [^\n]*?\}(?:,| )\n*",
    # function形式
    r"\{\s*key:'(?:mahou|mahou_tentacle|tentacle|manga_mahou|mahou_age|mahou_jk|manga_mahou_jc|manga_mahou_jk)',\s*label:'[^']*',\s*fn: function\(id\)\{[^\n]*?\} \},\n*",
]
tot = 0
for p in patterns:
    s, n = re.subn(p, '', s)
    tot += n
    print('gd pattern removed:', n)
print('total gd removed:', tot)

# grp_manga_mahou 大グループ
s, ng = re.subn(r"\{\s*key:'grp_manga_mahou',\s*label:\"[^\"]*\",\s*icon:'[^']*',\s*\n*\s*cats:\[[^\]]*\]\s*\},\n*", '', s)
print('grp_manga_mahou removed:', ng)

# 残存id定義チェック
rest = re.findall(r"id[\"']?\s*:\s*[\"'](char_(?:mahou_shoujo_|mahou_(?:youjo|shougaku|chuugaku|jk|youchien)_|manga_mahou_|tentacle_(?:youjo|shougaku|chuugaku|elf|mahou|nurse)_)[a-zA-Z0-9_]*)[\"']", s)
print('remaining char defs:', len(rest), rest[:5])
assert len(rest) == 0

m = re.search(r'name="version" content="(\d+)"', s)
old = m.group(1); new = str(int(old)+1)
s = s.replace(f'content="{old}"', f'content="{new}"', 1)
print('version:', old, '->', new)
open(DB, 'w', encoding='utf-8', newline='').write(s)
print('saved. size:', orig_len, '->', len(s))
for x in removed_ids:
    print('  removed:', x)
