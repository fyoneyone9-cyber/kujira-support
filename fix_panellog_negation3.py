import sys
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8') as f:
    content = f.read()

# 元のコピー処理
old = "navigator.clipboard.writeText(document.getElementById(\\'lp\\').textContent).then(function(){this.textContent=\\'" + "\u2705 \u30b3\u30d4\u30fc\u6e08" + "\\';}.bind(this))"

# 否定文生成+コピーする新処理
new = (
    "(function(btn){"
    "var txt=document.getElementById(\\'lp\\').textContent;"
    "try{"
    "var obj=JSON.parse(txt);"
    "var lbl=obj.outfit_label||obj.outfit_label_full||\\'\\';"
    "if(lbl){"
    "var m=lbl.match(/\u300b(.+)$/);"
    "var phrase=m?m[1]:lbl;"
    "var neg;"
    "if(/[\u3046\u304f\u3059\u3064\u306c\u3075\u3080\u3086\u308b\u3092]$/.test(phrase)){neg=phrase+\\'\u3066\u3044\u306a\u3044\\';}
"
    "else if(/\u3044$/.test(phrase)){neg=phrase.slice(0,-1)+\\'\u304f\u306a\u3044\\';}
"
    "else{neg=phrase+\\'\u3057\u3066\u3044\u306a\u3044\\';}
"
    "txt=txt+\\'\\\\n\\'+lbl+\\'\\\\n\\'+neg;"
    "}"
    "}catch(e){}"
    "navigator.clipboard.writeText(txt).then(function(){btn.textContent=\\'" + "\u2705 \u30b3\u30d4\u30fc\u6e08" + "\\';});"
    "}(this))"
)

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK")
else:
    print("NOT FOUND")
    # デバッグ: 実際の文字列を確認
    idx = content.find("navigator.clipboard.writeText(document.getElementById(\\'lp\\').textContent)")
    print(f"marker at {idx}")
    if idx != -1:
        snippet = content[idx:idx+150]
        print(repr(snippet))
