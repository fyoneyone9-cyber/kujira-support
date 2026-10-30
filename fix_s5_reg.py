import sys, re
sys.stdout.reconfigure(encoding='utf-8')

html_path = r'C:\AI\ComfyUI\dashboard.html'
with open(html_path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# 壊れたエントリを削除（'kaizo_nichijou4', 'kaizo_nichijou5' のダブルキー）
bad = "{key:'kaizo_nichijou4', 'kaizo_nichijou5',label:\"🏠💉🔥狂気改造S5\",fn:id => /^char_kaizo_nichijou5_/.test(id),bigGenre:'💉 改造・洗脳'},"
if bad in content:
    content = content.replace(bad, "")
    print("壊れたエントリ削除OK")
else:
    print("壊れたエントリ見つからず（既に削除済み or 形式違い）")

# S5の registerGenre が既にあるか
if "kaizo_nichijou5" in content and "registerGenre" in content:
    # 既存を確認
    m = re.search(r"registerGenre\(\{key:'kaizo_nichijou5'[^}]+\}\);", content)
    if m:
        print(f"S5 registerGenre 既存: {m.group()[:100]}")
    else:
        print("S5 registerGenre なし → 追加する")
        # S4のregisterGenreの直後に追加
        s4_reg = "registerGenre({key:'kaizo_nichijou4',label:'🏠💉🔥狂気改造S4',pattern:/^char_kaizo_nichijou4_/,bigGenre:'💉 改造・洗脳',categoryGroup:'grp_kaizo'});"
        s5_reg = "\nregisterGenre({key:'kaizo_nichijou5',label:'🏠💉🔥狂気改造S5',pattern:/^char_kaizo_nichijou5_/,bigGenre:'💉 改造・洗脳',categoryGroup:'grp_kaizo'});"
        if s4_reg in content:
            content = content.replace(s4_reg, s4_reg + s5_reg)
            print("S5 registerGenre 追加OK")
        else:
            print("S4 registerGenreが見つからない")
else:
    print("S5 追加が必要")
    s4_reg = "registerGenre({key:'kaizo_nichijou4',label:'🏠💉🔥狂気改造S4',pattern:/^char_kaizo_nichijou4_/,bigGenre:'💉 改造・洗脳',categoryGroup:'grp_kaizo'});"
    s5_reg = "\nregisterGenre({key:'kaizo_nichijou5',label:'🏠💉🔥狂気改造S5',pattern:/^char_kaizo_nichijou5_/,bigGenre:'💉 改造・洗脳',categoryGroup:'grp_kaizo'});"
    if s4_reg in content:
        content = content.replace(s4_reg, s4_reg + s5_reg)
        print("S5 registerGenre 追加OK")
    else:
        print("S4 registerGenreが見つからない")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(content)

# 確認
print("\n=== 確認 ===")
with open(html_path, encoding='utf-8', errors='replace') as f:
    content2 = f.read()
for m in re.finditer(r"registerGenre\(\{key:'kaizo_nichijou[45]'[^\n]+", content2):
    print(m.group()[:150])
