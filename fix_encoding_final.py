import subprocess, os

# gitのblobをバイナリで取得
result = subprocess.run(
    ['C:\\Program Files\\Git\\cmd\\git.exe', 'cat-file', 'blob', '18f92a49b713c0520b8bcf26b9d8a09badd170fb'],
    cwd=r'C:\Users\fyone\Desktop\kujira-support',
    capture_output=True
)
raw = result.stdout
print('raw bytes[:20]:', raw[:20])

# エンコーディング判定
for enc in ['utf-8', 'utf-8-sig', 'shift-jis', 'cp932']:
    try:
        text = raw.decode(enc)
        if 'cat_busy' in text and '今は忙しい' in text:
            print(f'correct encoding: {enc}')
            break
        else:
            print(f'{enc}: decoded but no Japanese match')
    except Exception as e:
        print(f'{enc}: failed - {e}')
