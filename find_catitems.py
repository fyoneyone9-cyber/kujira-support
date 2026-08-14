with open(r'C:\Users\fyone\Desktop\teleapo_orig.tsx', 'r', encoding='utf-8-sig') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'CATEGORY_ITEMS' in l and ('const' in l or '=' in l):
        print(i+1, l.rstrip()[:120])
        for j in range(i, min(i+60, len(lines))):
            print(j+1, lines[j].rstrip()[:120])
        break
