import sys, re
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8') as f:
    content = f.read()

old = r"""onclick="navigator.clipboard.writeText(document.getElementById(\'lp\').textContent).then(function(){this.textContent=\'✅ コピー済\';}.bind(this))""""

new = r"""onclick="(function(btn){var txt=document.getElementById(\'lp\').textContent;try{var obj=JSON.parse(txt);var lbl=obj.outfit_label||obj.outfit_label_full||\'\';var neg=\'\';if(lbl){var m=lbl.match(/】(.+)$/);var phrase=m?m[1]:lbl;if(/[うくすつぬふむゆるを]$/.test(phrase)){neg=phrase+\'ていない\';}else if(/[い]$/.test(phrase)){neg=phrase.slice(0,-1)+\'くない\';}else if(/[だ]$/.test(phrase)){neg=phrase.slice(0,-1)+\'でない\';}else{neg=phrase+\'していない\';}neg=\'\n\'+lbl+\'\\n\'+neg;}txt=txt+neg;}catch(e){}navigator.clipboard.writeText(txt).then(function(){btn.textContent=\'✅ コピー済\';});}(this))""""

if old in content:
    content = content.replace(old, new, 1)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("OK: replaced")
else:
    print("ERROR: not found, trying alternate search...")
    idx = content.find("navigator.clipboard.writeText(document.getElementById(\\'lp\\')")
    print(f"idx={idx}")
    if idx != -1:
        print(repr(content[idx-20:idx+200]))
