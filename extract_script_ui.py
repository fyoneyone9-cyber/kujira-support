with open(r'C:\Users\fyone\Desktop\teleapo_orig.tsx', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

# scriptタブのUI（580〜1073行）を表示して構造確認
script_lines = lines[579:650]
for i, l in enumerate(script_lines, 580):
    print(i, l.rstrip()[:100])
