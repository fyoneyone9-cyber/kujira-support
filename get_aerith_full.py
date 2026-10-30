import sys, io, re, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()

# char_kakuseizai_s3_ff_aerith を探す
idx = content.find('char_kakuseizai_s3_ff_aerith')
if idx == -1:
    print('NOT FOUND')
    sys.exit(1)

# そのブロックの前後2000文字を取得
chunk = content[max(0,idx-100):idx+3000]
print(chunk[:3000])
