import sys, os
sys.stdout.reconfigure(encoding='utf-8')

src = r'C:\Users\fyone\Downloads\【工程管理】泰和アルン淀屋橋 - NW関連.csv'
for enc in ['utf-8-sig', 'shift_jis', 'cp932']:
    try:
        with open(src, encoding=enc) as f:
            content = f.read(5000)
        print(f'encoding: {enc}')
        print(content)
        break
    except Exception as e:
        print(f'{enc}: {e}')
