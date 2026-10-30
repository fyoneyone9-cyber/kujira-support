import sys, re
sys.stdout.reconfigure(encoding='utf-8')
path = r'C:\AI\ComfyUI\dashboard.html'
with open(path, encoding='utf-8', errors='replace') as f:
    content = f.read()

tifa = content.find("char_kakuseizai_tifa'")
oi = content.find('outfits:[', tifa)
first = content.find("'label':", oi)
val_start = content.find("'value':'", first)
val_end = content.find("'}", val_start + 9)
val = content[val_start+9:val_end]
print("tifa scene 00 value:")
print(val[:600])
