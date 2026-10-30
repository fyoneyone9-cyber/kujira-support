import sys, io, json, requests
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 直近のapi_server.logからmoody_zitに関するKSAMPLERログを探す
with open(r'C:\AI\ComfyUI\api_server.log', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

# 直近200行でKSAMPLER/CFG/moody_zit関連を抽出
hits = []
for i, l in enumerate(lines[-500:]):
    if any(k in l for k in ['KSAMPLER', 'cfg=', 'moody_zit', 'KREA2_KSAMPLER', 'NON_QW21', 'zit']):
        hits.append(l.rstrip())

for h in hits[-30:]:
    print(h)
