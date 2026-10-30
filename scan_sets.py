import json,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=json.load(open(r'C:\AI\ComfyUI\outfit_sets.json',encoding='utf-8'))
print('keys:',len(d))
k='S0432'
if k in d:
    a=d[k]
    print(k,'len',len(a))
    print(json.dumps(a[:3],ensure_ascii=False,indent=1)[:1500])
