import re,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
s=open(r'C:\AI\ComfyUI\dashboard.html',encoding='utf-8').read()
hits=[m.start() for m in re.finditer(r'S0432', s)]
print('count', len(hits), hits[:5], hits[-5:])
m=re.search(r"S0432['\"]?\s*[:=]", s)
print('defsearch:', m.start() if m else None)
# look at first occurrence context
print(s[hits[0]-300:hits[0]+500])
