import re
c = open(r'C:\AI\ComfyUI\dashboard.html','r',encoding='utf-8').read()
m = re.search(r"name=['\"]version['\"] content=['\"](\d+)['\"]", c)
print('version:', m.group(1) if m else 'not found')
print('size:', len(c))
# 1792677738 が含まれるか
print('has_1792677738:', '1792677738' in c)
