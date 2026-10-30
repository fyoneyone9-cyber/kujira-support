import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(r'C:\AI\ComfyUI\dashboard.html', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

for char_id in ['char_rape_ff_tifa', 'char_rape_ff_aerith']:
    idx = content.find(f"'{char_id}'")
    push_start = content.rfind('window.CHAR_TEMPLATES.female.push({', 0, idx)
    push_end = content.find('});', idx) + 3
    block = content[push_start:push_end]
    
    print(f'=== {char_id} ===')
    # lora1, patterns, 最初のoutfit label を確認
    lora_m = re.search(r"lora1[^,\n]{0,100}", block)
    pat_m = re.search(r"patterns[^,\n]{0,50}", block)
    first_label = re.search(r'label:"([^"]{1,60})"', block)
    last_label = None
    for m in re.finditer(r'label:"([^"]{1,60})"', block):
        last_label = m.group(1)
    
    print(f'  lora1: {lora_m.group(0) if lora_m else "NOT FOUND"}')
    print(f'  patterns: {pat_m.group(0) if pat_m else "NOT FOUND"}')
    print(f'  first label: {first_label.group(1) if first_label else "?"}')
    print(f'  last label: {last_label}')
    
    # outfit valueのサンプル
    vals = re.findall(r'value:"([^"]{1,100})"', block)
    print(f'  outfit[0] value先頭: {vals[0][:120] if vals else "?"}')
    print()
