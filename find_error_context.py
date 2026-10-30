import re, sys
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = re.findall(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE)

# Block17: line 65059 = 65058 (0-indexed)
lines17 = scripts[17].split('\n')
print("Block17 lines 65054-65065:")
for j in range(65053, 65066):
    if j < len(lines17): print(j+1, repr(lines17[j][:100]))

# Block22: line 203 = 202 (0-indexed)  
lines22 = scripts[22].split('\n')
print("\nBlock22 lines 196-210:")
for j in range(195, 211):
    if j < len(lines22): print(j+1, repr(lines22[j][:100]))
