import re, json, sys
s = open(r'C:\AI\ComfyUI\dashboard.html', encoding='utf-8', errors='ignore').read()
sets = json.load(open(r'C:\AI\ComfyUI\outfit_sets.json', encoding='utf-8'))
cid = sys.argv[1]
m = re.search(r"id:\s*'" + re.escape(cid) + r"'", s)
if not m:
    print('NOT FOUND'); sys.exit()
block = s[m.start()-20:m.start()+3000]
rm = re.search(r'outfits_ref\s*:\s*"([^"]+)"', block)
print('ref:', rm.group(1) if rm else None, '| in json:', rm and rm.group(1) in sets)
print('inline outfits:', bool(re.search(r'outfits\s*:\s*\[', block)))
print(block[:800])
