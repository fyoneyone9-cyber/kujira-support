import sys, csv
sys.stdout.reconfigure(encoding='utf-8')

path = r'C:\Users\fyone\Downloads\【工程管理】泰和アルン淀屋橋 - NW関連.csv'
with open(path, encoding='utf-8-sig') as f:
    rows = list(csv.reader(f))

print(f'rows: {len(rows)}')
for i, r in enumerate(rows[:3]):
    print(f'row{i}: {r}')
print('...')
print(f'row-1: {rows[-1]}')
