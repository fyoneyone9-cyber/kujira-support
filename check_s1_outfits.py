import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

# S1 jk_Aのoutfitsを力技で探す
# outfitsキーワードが見つからない場合、scenesまたは別のキーかも
idx = content.find("char_kakuseizai_jk_A'")
if idx < 0:
    idx = content.find('char_kakuseizai_jk_A')
chunk = content[idx:idx+5000]
print(chunk[:2000])
