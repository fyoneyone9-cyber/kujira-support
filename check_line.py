import re, sys, subprocess, tempfile, os
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()
print("Line 74445-74455:")
for j in range(74444, 74456):
    if j < len(lines): print(j+1, repr(lines[j][:120]))
