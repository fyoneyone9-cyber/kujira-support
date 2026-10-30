"""
tifa/aerith/peach/mitsuri を S1/S2/S3 に正しい push() 形式で追加。
各ブロックの末尾（最後のchar_kakuseizai_*_C の }); の後）に挿入。
"""
import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

def find_char_end(content, char_id):
    """charのpushブロック終端（});の位置 + 3）を返す"""
    idx = content.find(char_id)
    if idx < 0: return -1
    end = content.find('});', idx)
    return end + 3  # }); の後

def make_push(obj_str):
    return '\nwindow.CHAR_TEMPLATES.female.push(' + obj_str + ');\n'

# ===== S1 chars: tifa / aerith / peach / mitsuri =====
# jk_C の後に挿入
jkc_end = find_char_end(content, "char_kakuseizai_jk_C")
print(f"jk_C end at: {jkc_end}")

S1_TIFA = """{
  id:'char_kakuseizai_tifa',label:"💊覚醒剤S1 👊ティファ",gender:'female',
  prompt:'(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(long black hair:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),(black mini dress:1.2),(leather suspenders:1.1)',
  neg:'(adult:1.3),(mature:1.4),(middle aged:1.5),watermark,signature,text,logo,multiple girls',
  outfits:[{'label':'00 「炙り」ホイルで炙り吸引','value':'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(long black hair:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),(black mini dress:1.2),(leather suspenders:1.1),holding aluminum foil with both hands at chest level,drug crystal on foil held in hands,lighter held beneath foil in hands,lighter flame heating foil from below in hands,white smoke rising upward from foil,face leaning toward smoke,inhaling through straw,foil held at waist to chest height,drug paraphernalia in hands,dazed expression starting,flushed cheeks beginning,upper body shot,dim room,eye level,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{'label':'28 「廃人」快楽漬け','value':'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(long black hair:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),(black mini dress:1.2),(leather suspenders:1.1),fully nude,broken empty expression,ahegao permanent,drooling,lying limp covered in cum,full body,dim room,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6),(heavy breathing:1.5),(euphoric:1.6),(ahegao:1.4),(rolling eyes:1.3),(drooling:1.4)'}]
}"""

S1_AERITH = """{
  id:'char_kakuseizai_aerith',label:"💊覚醒剤S1 🌿エアリス",gender:'female',
  prompt:'(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail pink ribbon:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2)',
  neg:'(adult:1.3),(mature:1.4),(middle aged:1.5),watermark,signature,text,logo,multiple girls',
  outfits:[{'label':'00 「炙り」ホイルで炙り吸引','value':'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2),holding aluminum foil with both hands at chest level,drug crystal on foil held in hands,lighter held beneath foil in hands,lighter flame heating foil from below in hands,white smoke rising upward from foil,face leaning toward smoke,inhaling through straw,foil held at waist to chest height,drug paraphernalia in hands,dazed expression starting,flushed cheeks beginning,upper body shot,dim room,eye level,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{'label':'28 「廃人」快楽漬け','value':'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2),fully nude,broken empty expression,ahegao permanent,drooling,lying limp covered in cum,full body,dim room,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6),(heavy breathing:1.5),(euphoric:1.6),(ahegao:1.4),(rolling eyes:1.3),(drooling:1.4)'}]
}"""

S1_PEACH = """{
  id:'char_kakuseizai_peach',label:"💊覚醒剤S1 👸ピーチ姫",gender:'female',
  prompt:'(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),(pink princess dress:1.2),(golden crown:1.1)',
  neg:'(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,text,logo,multiple girls',
  outfits:[{'label':'00 「炙り」ホイルで炙り吸引','value':'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),(pink princess dress:1.2),(golden crown:1.1),holding aluminum foil with both hands at chest level,drug crystal on foil held in hands,lighter held beneath foil in hands,lighter flame heating foil from below in hands,white smoke rising upward from foil,face leaning toward smoke,inhaling through straw,foil held at waist to chest height,drug paraphernalia in hands,dazed expression starting,flushed cheeks beginning,upper body shot,dim room,eye level,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{'label':'28 「廃人」快楽漬け','value':'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),fully nude,broken empty expression,ahegao permanent,drooling,lying limp covered in cum,full body,dim room,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6),(heavy breathing:1.5),(euphoric:1.6),(ahegao:1.4),(rolling eyes:1.3),(drooling:1.4)'}]
}"""

S1_MITSURI = """{
  id:'char_kakuseizai_mitsuri',label:"💊覚醒剤S1 🌸甘露寺蜜璃",gender:'female',
  prompt:'(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(pink haori:1.1),(revealing uniform:1.1)',
  neg:'(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls',
  outfits:[{'label':'00 「炙り」ホイルで炙り吸引','value':'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(pink haori:1.1),(revealing uniform:1.1),holding aluminum foil with both hands at chest level,drug crystal on foil held in hands,lighter held beneath foil in hands,lighter flame heating foil from below in hands,white smoke rising upward from foil,face leaning toward smoke,inhaling through straw,foil held at waist to chest height,drug paraphernalia in hands,dazed expression starting,flushed cheeks beginning,upper body shot,dim room,eye level,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{'label':'28 「廃人」快楽漬け','value':'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(pink haori:1.1),(revealing uniform:1.1),fully nude,broken empty expression,ahegao permanent,drooling,lying limp covered in cum,full body,dim room,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6),(heavy breathing:1.5),(euphoric:1.6),(ahegao:1.4),(rolling eyes:1.3),(drooling:1.4)'}]
}"""

# S1を jk_C の後に一括挿入
s1_insert = make_push(S1_TIFA) + make_push(S1_AERITH) + make_push(S1_PEACH) + make_push(S1_MITSURI)
content = content[:jkc_end] + s1_insert + content[jkc_end:]
print("S1 chars inserted")

# ===== S2: usagi の後に s2_peach / s2_mitsuri を追加 =====
# S2の末尾: char_kakuseizai_s2_rei の後（または s2_usagi/s2_tifa/s2_aerith/s2_asuka/s2_rei）
# S2の最後のキャラを探す
for s2_last_id in ['char_kakuseizai_s2_rei', 'char_kakuseizai_s2_asuka', 'char_kakuseizai_s2_aerith']:
    pos = find_char_end(content, s2_last_id)
    if pos > 0:
        print(f"S2 last char end: {s2_last_id} at {pos}")
        break

S2_PEACH = """{
  id:'char_kakuseizai_s2_peach',label:"💊覚醒剤S2 👸ピーチ姫",gender:'female',
  prompt:'Princess Peach,Super Mario,blonde hair,blue eyes,medium breasts,slender body,pink princess dress,golden crown',
  neg:'(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls',
  outfits:[{label:'00「強制摂取」錠剤を無理やり飲ませられる',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),(pink princess dress:1.2),(golden crown:1.1),forced to swallow pill,hand on jaw forcing mouth open,tears streaming,held from behind,pill on tongue,upper body,dim light,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{label:'29 「廃人化」完全崩壊',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),fully nude,broken expression,permanent ahegao,drooling,lying limp,cum covered,full body,dim room,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6)'}]
}"""

S2_MITSURI = """{
  id:'char_kakuseizai_s2_mitsuri',label:"💊覚醒剤S2 🌸甘露寺蜜璃",gender:'female',
  prompt:'(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1)',
  neg:'(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls',
  outfits:[{label:'00「強制摂取」錠剤を無理やり飲ませられる',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1),forced to swallow pill,hand on jaw forcing mouth open,tears streaming,held from behind,pill on tongue,upper body,dim light,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{label:'29 「廃人化」完全崩壊',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1),fully nude,broken expression,permanent ahegao,drooling,lying limp,cum covered,full body,dim room,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6)'}]
}"""

if pos > 0:
    s2_insert = make_push(S2_PEACH) + make_push(S2_MITSURI)
    content = content[:pos] + s2_insert + content[pos:]
    print("S2 peach/mitsuri inserted")

# ===== S3: ff_aerith の後に s3_peach / s3_mitsuri を追加 =====
for s3_last_id in ['char_kakuseizai_s3_ff_aerith', 'char_kakuseizai_s3_ff_tifa']:
    pos3 = find_char_end(content, s3_last_id)
    if pos3 > 0:
        print(f"S3 last char end: {s3_last_id} at {pos3}")
        break

S3_PEACH = """{
  id:'char_kakuseizai_s3_peach',label:"💊覚醒剤S3 👸ピーチ姫",gender:'female',
  prompt:'(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),(pink princess dress:1.2),(golden crown:1.1)',
  neg:'(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls',
  outfits:[{label:'00 「強制投与」注射で一気に廃人化',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),(pink princess dress:1.2),restrained,syringe forced into arm vein,wide terror eyes,trembling,upper body,dim room,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{label:'29 「廃棄」完全廃人・廃棄される',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),fully nude,permanent hollow expression,dead eyes,cum all over,abandoned in room,full body,dirty floor,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6)'}]
}"""

S3_MITSURI = """{
  id:'char_kakuseizai_s3_mitsuri',label:"💊覚醒剤S3 🌸甘露寺蜜璃",gender:'female',
  prompt:'(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1)',
  neg:'(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls',
  outfits:[{label:'00 「強制投与」注射で一気に廃人化',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1),restrained,syringe forced into arm vein,wide terror eyes,trembling,upper body,dim room,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{label:'29 「廃棄」完全廃人・廃棄される',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1),fully nude,permanent hollow expression,dead eyes,cum all over,abandoned in room,full body,dirty floor,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6)'}]
}"""

if pos3 > 0:
    s3_insert = make_push(S3_PEACH) + make_push(S3_MITSURI)
    content = content[:pos3] + s3_insert + content[pos3:]
    print("S3 peach/mitsuri inserted")

# バージョン更新
ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_addchars_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

# JS check
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)
errors = []
for i, sc in enumerate(scripts):
    sc2 = sc.strip()
    if not sc2 or len(sc2) < 20: continue
    tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False, encoding='utf-8')
    tmp.write(sc2); tmp.close()
    r = subprocess.run(['node', '--check', tmp.name], capture_output=True, timeout=15)
    os.unlink(tmp.name)
    err = r.stderr.decode('utf-8', errors='replace') if r.stderr else ''
    if r.returncode != 0:
        errors.append((i, err))
print("Remaining JS errors:", len(errors))
for i, err in errors[:5]:
    print("  block", i, ":", err[:200])
