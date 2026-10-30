import re,sys
sys.stdout.reconfigure(encoding='utf-8',errors='replace')
s=open(r'C:\AI\ComfyUI\dashboard.html',encoding='utf-8').read()
m=re.search(r"id:\s*'char_babyreg_s1_aerith'",s)
print(s[m.start()-50:m.start()+3400])
