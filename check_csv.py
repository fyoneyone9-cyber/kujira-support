import csv, sys
sys.stdout.reconfigure(encoding='utf-8')
files = [
    r'C:\Users\fyone\Downloads\【管理】IoT製品納品一覧 - 納品管理.csv',
    r'C:\Users\fyone\Downloads\【管理】IoT製品納品一覧 - 納品管理（進行中）.csv',
]
headers = []
for fp in files:
    with open(fp, encoding='shift-jis', errors='replace') as f:
        rows = list(csv.reader(f))
    # ヘッダーは複数行にまたがる可能性あり(multiline)。row[0]だけ見る
    h = rows[0]
    headers.append(h)
    name = '納品管理' if '進行' not in fp else '進行中'
    print(f'\n=== {name} ({len(h)}列) ===')
    for i, col in enumerate(h):
        col_clean = col.replace('\n','\\n')
        print(f'  [{i:2d}] {col_clean}')

print('\n=== 差分（進行中にあって納品管理にない列） ===')
h1_set = set(h.replace('\n','') for h in headers[0])
for i, col in enumerate(headers[1]):
    col_clean = col.replace('\n','')
    if col_clean not in h1_set:
        print(f'  [{i:2d}] {col_clean}')
