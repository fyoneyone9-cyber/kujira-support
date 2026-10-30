import sys
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
cid = sys.argv[1]
i = s.find("'" + cid + "'")
print('found at', i)
print(s[max(0,i-100):i+3000])
