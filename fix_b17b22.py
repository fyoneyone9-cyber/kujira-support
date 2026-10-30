import re, sys, shutil, datetime, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()
scripts = list(re.finditer(r'<script(?:\s[^>]*)?>(.+?)</script>', content, re.DOTALL | re.IGNORECASE))

# Block17: line 65058 に余分な });
sc17 = scripts[17]
lines17 = sc17.group(1).split('\n')
print("Block17 65054-65063:")
for j in range(65053, 65064):
    if j < len(lines17): print(j+1, repr(lines17[j][:100]))

# Block22: line 153 の } エラー
sc22 = scripts[22]
lines22 = sc22.group(1).split('\n')
print("\nBlock22 148-158:")
for j in range(147, 159):
    if j < len(lines22): print(j+1, repr(lines22[j][:100]))
