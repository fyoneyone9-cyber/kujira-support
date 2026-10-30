import re, io
p = r'C:\AI\ComfyUI\dashboard.html'
s = io.open(p, 'r', encoding='utf-8').read()
# fetch url of OUTFIT_SETS
i = s.find('[OUTFIT_SETS] load failed')
print(s[max(0,i-1500):i+100])
print('='*60)
# context of "S06 occurrence (embedded JSON?)
st = 10968344
print(s[st-800:st+800])
