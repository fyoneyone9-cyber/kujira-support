import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

def find_char_end(content, char_id):
    idx = content.find(char_id)
    if idx < 0: return -1
    end = content.find('});', idx)
    return end + 3

def make_push(obj_str):
    return '\nwindow.CHAR_TEMPLATES.female.push(' + obj_str + ');\n'

s3jkc_end = find_char_end(content, 'char_kakuseizai_s3_jk_C')
print("s3_jk_C end:", s3jkc_end)

S3_FF_TIFA = """{
  id:'char_kakuseizai_s3_ff_tifa',label:"💊覚醒剤S3 👊ティファ",gender:'female',
  prompt:'(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(long black hair:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),(black mini dress:1.2),(leather suspenders:1.1)',
  neg:'(adult:1.3),(mature:1.4),(middle aged:1.5),watermark,signature,text,logo,multiple girls',
  outfits:[{label:'00 「強制投与」注射で一気に廃人化',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(long black hair:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),(black mini dress:1.2),(leather suspenders:1.1),restrained,syringe forced into arm vein,wide terror eyes,trembling,upper body,dim room,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{label:'29 「廃棄」完全廃人・廃棄される',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Tifa Lockhart:1.5),(Final Fantasy VII:1.35),(long black hair:1.3),(red eyes:1.2),(large breasts:1.6),(athletic body:1.4),fully nude,permanent hollow expression,dead eyes,cum all over,abandoned in room,full body,dirty floor,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6)'}]
}"""

S3_FF_AERITH = """{
  id:'char_kakuseizai_s3_ff_aerith',label:"💊覚醒剤S3 🌿エアリス",gender:'female',
  prompt:'(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail pink ribbon:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2)',
  neg:'(adult:1.3),(mature:1.4),(middle aged:1.5),watermark,signature,text,logo,multiple girls',
  outfits:[{label:'00 「強制投与」注射で一気に廃人化',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2),restrained,syringe forced into arm vein,wide terror eyes,trembling,upper body,dim room,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{label:'29 「廃棄」完全廃人・廃棄される',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Aerith Gainsborough:1.5),(Final Fantasy VII:1.35),(light brown hair ponytail:1.3),(green eyes:1.2),(medium breasts:1.35),(slender body:1.3),(pink dress:1.2),fully nude,permanent hollow expression,dead eyes,cum all over,abandoned in room,full body,dirty floor,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6)'}]
}"""

S3_PEACH = """{
  id:'char_kakuseizai_s3_peach',label:"💊覚醒剤S3 👸ピーチ姫",gender:'female',
  prompt:'(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),(pink princess dress:1.2),(golden crown:1.1)',
  neg:'(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls',
  outfits:[{label:'00 「強制投与」注射で一気に廃人化',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),(pink princess dress:1.2),(golden crown:1.1),restrained,syringe forced into arm vein,wide terror eyes,trembling,upper body,dim room,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{label:'29 「廃棄」完全廃人・廃棄される',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Princess Peach:1.5),(Super Mario:1.35),(blonde hair:1.3),(blue eyes:1.2),(medium breasts:1.4),(slender body:1.3),fully nude,permanent hollow expression,dead eyes,cum all over,abandoned in room,full body,dirty floor,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6)'}]
}"""

S3_MITSURI = """{
  id:'char_kakuseizai_s3_mitsuri',label:"💊覚醒剤S3 🌸甘露寺蜜璃",gender:'female',
  prompt:'(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1)',
  neg:'(adult:1.2),(mature:1.4),(middle aged:1.5),watermark,signature,multiple girls',
  outfits:[{label:'00 「強制投与」注射で一気に廃人化',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1),restrained,syringe forced into arm vein,wide terror eyes,trembling,upper body,dim room,(anatomically correct:1.5),(masterpiece:1.2),(best quality:1.2),detailed'},{label:'29 「廃棄」完全廃人・廃棄される',value:'(solo:2.2),(1girl:2.2),(only one person:2.0),(2girls:0.0),(multiple girls:0.0),(exactly one girl:1.6),(Kanroji Mitsuri:1.5),(Demon Slayer:1.35),(long pink green gradient hair:1.3),(green eyes:1.2),(large breasts:1.6),(voluptuous body:1.4),(love pillar uniform:1.2),(revealing uniform:1.1),fully nude,permanent hollow expression,dead eyes,cum all over,abandoned in room,full body,dirty floor,(drugged high:1.8),(dilated pupils:1.8),(flushed face:1.7),(sweating:1.6)'}]
}"""

s3_insert = make_push(S3_FF_TIFA) + make_push(S3_FF_AERITH) + make_push(S3_PEACH) + make_push(S3_MITSURI)
content = content[:s3jkc_end] + s3_insert + content[s3jkc_end:]
print("S3 chars inserted")

ver_m = re.search(r'content="(\d{10,})"', content)
if ver_m:
    old_ver = ver_m.group(1); new_ver = str(int(old_ver) + 1)
    content = content.replace('content="' + old_ver + '"', 'content="' + new_ver + '"', 1)
    print("Version:", old_ver, "->", new_ver)

shutil.copy2(path, r'C:\AI\ComfyUI\dashboard_backup_s3add_' + datetime.datetime.now().strftime('%Y%m%d_%H%M%S') + '.html')
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Saved.")

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
for i, err in errors[:3]:
    print("  block", i, ":", err[:150])
