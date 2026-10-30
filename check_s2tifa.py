import sys, re
sys.stdout.reconfigure(encoding='utf-8')
with open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='replace') as f:
    content = f.read()
idx = content.find("char_kakuseizai_s2_tifa'")
oi = content.find('outfits:[', idx)
s = content.find('[', oi)
print(repr(content[s:s+300]))
