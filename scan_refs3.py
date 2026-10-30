import re,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
s=open(r'C:\AI\ComfyUI\dashboard.html',encoding='utf-8').read()
# how is outfits_ref resolved?
for m in list(re.finditer(r'outfits_ref', s))[:3]:
    pass
# find code usage (not in push lines): look for 'outfits_ref' near '=' or function
for m in re.finditer(r'[^,{]outfits_ref[^:"]', s):
    print(m.start(), repr(s[m.start()-120:m.start()+250]))
    print('---')
