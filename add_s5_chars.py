import sys, re
sys.stdout.reconfigure(encoding='utf-8')

CHARS = [
    # S5 - 狂気改造S5（エアリス・ティファ+7体）
    {
        "id": "char_kaizo_nichijou5_aerith",
        "label": "🔥S5 エアリス【廃人堕ち】",
        "base_char": "Aerith Gainsborough,Final Fantasy VII,long brown hair with ribbon,green eyes,slender,22 years old",
        "body_mods": "nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,surgical scars,breeding marks",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(aerith gainsborough:1.9),(final fantasy:1.8),(ff7:1.8),(廃人:1.9),(completely destroyed soul:2.0)",
        "outfits_ref": "S0256"
    },
    {
        "id": "char_kaizo_nichijou5_tifa",
        "label": "🔥S5 ティファ【廃人堕ち】",
        "base_char": "Tifa Lockhart,Final Fantasy VII,long black hair,red eyes,athletic body,22 years old,large breasts",
        "body_mods": "nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,surgical scars,breeding marks",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(tifa lockhart:1.9),(final fantasy:1.8),(ff7:1.8),(廃人:1.9),(completely destroyed soul:2.0)",
        "outfits_ref": "S0256"
    },
    {
        "id": "char_kaizo_nichijou5_jk_A",
        "label": "🔥S5 JK-A【廃人堕ち】",
        "base_char": "japanese high school girl,17 years old,short black hair,brown eyes,slender,school uniform removed",
        "body_mods": "nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,surgical scars",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(廃人:1.9),(completely destroyed soul:2.0),(no longer human:1.9)",
        "outfits_ref": "S0256"
    },
    {
        "id": "char_kaizo_nichijou5_jk_B",
        "label": "🔥S5 JK-B【廃人堕ち】",
        "base_char": "japanese high school girl,16 years old,long brown hair,black eyes,petite,school uniform removed",
        "body_mods": "nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,surgical scars",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(廃人:1.9),(completely destroyed soul:2.0),(no longer human:1.9)",
        "outfits_ref": "S0256"
    },
    {
        "id": "char_kaizo_nichijou5_jk_C",
        "label": "🔥S5 JK-C【廃人堕ち】",
        "base_char": "japanese high school girl,17 years old,medium black hair,dark eyes,slim,school uniform removed",
        "body_mods": "nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification,surgical scars",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(廃人:1.9),(completely destroyed soul:2.0),(no longer human:1.9)",
        "outfits_ref": "S0256"
    },
    {
        "id": "char_kaizo_nichijou5_jc_A",
        "label": "🔥S5 JC-A【廃人堕ち】",
        "base_char": "japanese junior high school girl,14 years old,short black hair,brown eyes,petite,small breasts",
        "body_mods": "nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(廃人:1.9),(completely destroyed soul:2.0),(no longer human:1.9)",
        "outfits_ref": "S0256"
    },
    {
        "id": "char_kaizo_nichijou5_jc_B",
        "label": "🔥S5 JC-B【廃人堕ち】",
        "base_char": "japanese junior high school girl,13 years old,long brown hair,black eyes,petite,flat chest",
        "body_mods": "nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(廃人:1.9),(completely destroyed soul:2.0),(no longer human:1.9)",
        "outfits_ref": "S0256"
    },
    {
        "id": "char_kaizo_nichijou5_jc_C",
        "label": "🔥S5 JC-C【廃人堕ち】",
        "base_char": "japanese junior high school girl,14 years old,medium black hair,brown eyes,slim,flat chest",
        "body_mods": "nipple piercings,vaginal piercings,clitoral piercing,navel piercing,full body tattoos,ownership brand mark,slave collar,body modification",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(廃人:1.9),(completely destroyed soul:2.0),(no longer human:1.9)",
        "outfits_ref": "S0256"
    },
    {
        "id": "char_kaizo_nichijou5_js_A",
        "label": "🔥S5 JS-A【廃人堕ち】",
        "base_char": "japanese elementary school girl,11 years old,short black hair,brown eyes,petite,very small body,flat chest",
        "body_mods": "collar,ownership brand mark,slave collar,body modification marks",
        "mind_state": "(brainwashed:2.0),(mindbroken:2.0),(conditioned:2.0),(shattered will:1.9),(廃人:1.9),(completely destroyed soul:2.0),(no longer human:1.9)",
        "outfits_ref": "S0256"
    },
]

# dashboard.html を読み込んで </script> の直前に push() を追加
html_path = r'C:\AI\ComfyUI\dashboard.html'
with open(html_path, encoding='utf-8') as f:
    content = f.read()

# バージョン更新
ver_m = re.search(r'content="(\d+)"', content)
if ver_m:
    old_ver = ver_m.group(1)
    new_ver = str(int(old_ver) + 1)
    content = content.replace(f'content="{old_ver}"', f'content="{new_ver}"', 1)
    print(f"version: {old_ver} → {new_ver}")

# push()コードを生成
lines = []
for c in CHARS:
    char_prompt = f"{c['base_char']},{c['body_mods']},{c['mind_state']}"
    js = f"""window.CHAR_TEMPLATES.female.push({{
  id: '{c["id"]}',
  label: '{c["label"]}',
  char_prompt: {repr(char_prompt)},
  outfits_ref: '{c["outfits_ref"]}',
}});"""
    lines.append(js)

insert_code = "\n// [S5 chars added]\n" + "\n".join(lines) + "\n"

# block22の </script> の直前に挿入（S4と同じ場所）
# S4のpush末尾の後に挿入する
target = "// [S4 chars added]"
if target in content:
    # S4の後に追加
    s4_end = content.find("// [S4 chars added]")
    # S4ブロックの終わり（次の </script> まで）
    next_script = content.find("</script>", s4_end)
    content = content[:next_script] + insert_code + content[next_script:]
    print("S5 inserted after S4 block")
else:
    # 最後の </script> の直前
    last_script = content.rfind("</script>")
    content = content[:last_script] + insert_code + content[last_script:]
    print("S5 inserted before last </script>")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ {len(CHARS)}体追加完了")
