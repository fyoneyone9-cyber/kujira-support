import re
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
# where is S0273 defined (besides outfits_ref usage)?
for m in re.finditer(r'S0273', s):
    i = m.start()
    pre = s[i-40:i+10].replace('\n', '\\n')
    print(i, pre)
print('---')
# find the resolver code for outfits_ref
for m in re.finditer(r'outfits_ref', s):
    i = m.start()
    ctx = s[max(0,i-100):i+100].replace('\n','\\n')
    if 'push(' not in ctx:
        print('RESOLVER?', i, ctx)
