import json,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
d=json.load(open(r'C:\AI\ComfyUI\outfit_sets.json',encoding='utf-8'))
a=d['S0432']
print(type(a), list(a.keys()) if isinstance(a,dict) else len(a))
print(json.dumps(a,ensure_ascii=False,indent=1)[:2500])
