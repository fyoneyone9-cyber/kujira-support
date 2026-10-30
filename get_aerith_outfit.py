import re,sys,io,json,urllib.request
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html',encoding='utf-8',errors='replace') as f:
    content=f.read()

# char_kakuseizai_s3_ff_aerith のpush()ブロックを探す
idx=content.find("id:'char_kakuseizai_s3_ff_aerith'")
if idx<0:
    idx=content.find('id:"char_kakuseizai_s3_ff_aerith"')
if idx<0:
    idx=content.find('char_kakuseizai_s3_ff_aerith')
if idx<0:
    print('キャラ定義が見つからない'); sys.exit(1)

# 前後5000文字を取得してoutfit[0]のvalueを探す
chunk=content[idx:idx+8000]
m=re.search(r"value\s*:\s*['\"]([^'\"]{20,})['\"]",chunk)
if m:
    outfit0_value=m.group(1)
    print('outfit0 value (先頭200文字):')
    print(outfit0_value[:200])
else:
    print('value見つからない')
    sys.exit(1)

# 生成リクエスト送信
body=json.dumps({
    'page_idx':0,
    'panel_idx':0,
    'panel':{
        'char_template_id':'char_kakuseizai_s3_ff_aerith',
        'outfit_index':0,
        'prompt': outfit0_value,
        'style_preset':'moody_krea2_premium'
    }
}).encode('utf-8')

req=urllib.request.Request('http://127.0.0.1:3002/api/generate-panel',data=body,headers={'Content-Type':'application/json'},method='POST')
print('\n生成リクエスト送信中...')
try:
    with urllib.request.urlopen(req,timeout=300) as r:
        d=json.loads(r.read().decode('utf-8','replace'))
    print('完了:', d.get('image_path','(no path)'))
    pos=d.get('positive_prompt','')
    hits=[t.strip() for t in pos.split(',') if any(k in t for k in ['Aerith','Gainsborough','Final Fantasy','ff7','FF7'])]
    print('Aerith関連タグ in 最終プロンプト:', hits if hits else '0件（消えている）')
    if not hits:
        # dbg_qrも出力
        print('dbg_qr:', d.get('dbg_qr','')[:300])
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code, e.read().decode('utf-8','replace')[:300])
except Exception as e:
    print('Error:', e)
