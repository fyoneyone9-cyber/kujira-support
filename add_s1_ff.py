"""
覚醒剤S1 にティファ・エアリスを追加
S1のjk_Aのoutfitsを流用してキャラプロンプトだけ置換
"""
import sys, re, json, shutil, datetime
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# S1 jk_A の outfits を取得（JSON形式: {"label":"...","value":"..."}）
jka_idx = content.find("char_kakuseizai_jk_A'")
oi = content.find('outfits:[', jka_idx)
start = content.find('[', oi)
depth = 0
in_string = False
string_char = None
i = start
while i < len(content):
    c = content[i]
    if in_string:
        if c == '\\':
            i += 2
            continue
        if c == string_char:
            in_string = False
    else:
        if c in ('"', "'"):
            in_string = True
            string_char = c
        elif c == '[': depth += 1
        elif c == ']':
            depth -= 1
            if depth == 0:
                end = i + 1
                break
    i += 1

s1_outfits_raw = content[start:end]
# JSON形式のoutfits
outfits = re.findall(r'\{"label":\s*"([^"]+)",\s*"value":\s*"([^"]+)"\}', s1_outfits_raw)
print(f"S1 jk_A outfits: {len(outfits)}")

# キャラ置換関数
def make_ff_outfits_js(outfits, old_char_prompt, new_char_prompt, char_label):
    """S1のvalue内のキャラプロンプトを置換してJS形式で返す"""
    items = []
    for label, value in outfits:
        new_value = value.replace(old_char_prompt, new_char_prompt)
        label_esc = label.replace("'", "\\'")
        new_value_esc = new_value.replace("'", "\\'")
        items.append(f"{{'label':'{label_esc}','value':'{new_value_esc}'}}")
    return "[" + ",".join(items) + "]"

# S1 jk_A のキャラプロンプト（value内の特徴）
S1_CHAR_PROMPT = "(teenage girl:1.8),(young:1.7),(slender:1.6),(small breasts:1.5),(jk:1.6),16 years old,158cm,black long straight hair,school uniform"

# ティファ用
TIFA_CHAR_PROMPT = "(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(long black hair:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),(black mini dress:1.2),(leather suspenders:1.1)"

# エアリス用
AERITH_CHAR_PROMPT = "(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail pink ribbon:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2)"

tifa_outfits_js = make_ff_outfits_js(outfits, S1_CHAR_PROMPT, TIFA_CHAR_PROMPT, "ティファ")
aerith_outfits_js = make_ff_outfits_js(outfits, S1_CHAR_PROMPT, AERITH_CHAR_PROMPT, "エアリス")

print(f"Tifa outfits: {len(outfits)} scenes")
print(f"Aerith outfits: {len(outfits)} scenes")

# S1の最後のキャラクターの後に追加する
# char_kakuseizai_youchien_C の後ろを探す
# window.CHAR_TEMPLATES.female.push の直前にある既存S1キャラの最後を特定

# S1の終わりを特定（最後のS1キャラの直後）
# char_kakuseizai_youchien_C の後のブロックを探す
yc_idx = content.rfind("char_kakuseizai_youchien_C'")
if yc_idx < 0:
    yc_idx = content.rfind("char_kakuseizai_youchien_C")

print(f"youchien_C found at: {yc_idx}")

# youchien_C のキャラブロック全体の終端を探す
# }, または },\n{ で区切られている
block_end_search = content.find('\n},\n{', yc_idx)
if block_end_search < 0:
    block_end_search = content.find('\n},\n\n{', yc_idx)
print(f"block end candidate: {block_end_search}")
print(f"context: {content[block_end_search:block_end_search+50]!r}")

# S1の最後（ahegao_youchien_Cの後ろ）を確認
ahegao_yc = content.rfind("char_kakuseizai_ahegao_youchien_C'")
print(f"\nahegao_youchien_C at: {ahegao_yc}")
if ahegao_yc >= 0:
    # このキャラの終わりを探す
    # window.CHAR_TEMPLATES.female.push の次のブロック開始を探す
    after = content.find('window.CHAR_TEMPLATES.female.push', ahegao_yc)
    print(f"next push after ahegao_yc: {after}")
    if after >= 0:
        print(f"context: {content[after:after+100]!r}")

# S2の最初のキャラを探してその前に挿入
s2_first = content.find("char_kakuseizai_s2_")
print(f"\nS2 first char at: {s2_first}")
# S2の直前 = 挿入位置
# window.CHAR_TEMPLATES.female.push({id:'char_kakuseizai_s2_...' の行を探す
s2_push_idx = content.rfind('window.CHAR_TEMPLATES.female.push', 0, s2_first)
print(f"S2 push before s2_first: {s2_push_idx}")
print(f"context: {content[s2_push_idx:s2_push_idx+100]!r}")
