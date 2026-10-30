import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')

# 直近20件のタスクスケジューラ実行ログを取得
r = subprocess.run([
    'wevtutil', 'qe',
    'Microsoft-Windows-TaskScheduler/Operational',
    '/q:*[System[(EventID=200 or EventID=201)]]',
    '/c:30', '/rd:true', '/f:text'
], capture_output=True)
text = r.stdout.decode('cp932', errors='replace')
print(text[:8000])
