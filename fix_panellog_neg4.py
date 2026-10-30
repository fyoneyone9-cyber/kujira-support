import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8') as f:
    content = f.read()

# 元のコピー処理を特定（unicode escapeで書く）
copy_mark = "\u2705 \u30b3\u30d4\u30fc\u6e08"  # ✅ コピー済
sq = "\\'"  # \'  (HTMLのonclick内でのシングルクォートエスケープ)

old_str = (
    "navigator.clipboard.writeText(document.getElementById(" + sq + "lp" + sq + ").textContent)"
    ".then(function(){this.textContent=" + sq + copy_mark + sq + ";}.bind(this))"
)

print("Searching for old_str...")
idx = content.find(old_str)
print(f"idx = {idx}")

if idx == -1:
    # 実際にある文字列を確認
    i2 = content.find("navigator.clipboard.writeText(document.getElementById")
    print(f"partial match at {i2}")
    if i2 != -1:
        print(repr(content[i2:i2+250]))
    sys.exit(1)

# 新しい処理（JSをPython内でas-isで構築）
# outfit_labelの末尾動詞から否定形を作る
new_str = (
    "(function(btn){"
    "var txt=document.getElementById(" + sq + "lp" + sq + ").textContent;"
    "try{"
      "var obj=JSON.parse(txt);"
      "var lbl=obj.outfit_label||obj.outfit_label_full||'';"
      "if(lbl){"
        "var m=lbl.match(/\\u300b(.+)$/);"  # 】の後を取得
        "var phrase=m?m[1]:lbl;"
        "var neg;"
        # う/く/す/つ/ぬ/ふ/む/ゆ/る/を で終わるなら +ていない
        "if(/(\\u3046|\\u304f|\\u3059|\\u3064|\\u306c|\\u3075|\\u3080|\\u3086|\\u308b|\\u3092)$/.test(phrase)){"
          "neg=phrase+'\\u3066\\u3044\\u306a\\u3044';"  # ていない
        "}else if(/\\u3044$/.test(phrase)){"  # い
          "neg=phrase.slice(0,-1)+'\\u304f\\u306a\\u3044';"  # くない
        "}else{"
          "neg=phrase+'\\u3057\\u3066\\u3044\\u306a\\u3044';"  # していない
        "}"
        "txt=txt+'\\n'+lbl+'\\n'+neg;"
      "}"
    "}catch(e){}"
    "navigator.clipboard.writeText(txt).then(function(){btn.textContent=" + sq + copy_mark + sq + ";});"
    "}(this))"
)

content = content.replace(old_str, new_str, 1)
with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("OK: replaced")
