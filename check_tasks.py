import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
r = subprocess.run(['schtasks', '/Query', '/FO', 'LIST', '/V'], capture_output=True)
text = r.stdout.decode('cp932', errors='replace')
blocks = text.split('\n\n')
for b in blocks:
    lines = b.strip().splitlines()
    name = next((l for l in lines if 'タスク名' in l), '')
    cmd  = next((l for l in lines if '実行するタスク' in l), '')
    sch  = next((l for l in lines if 'スケジュールの種類' in l or '次回実行' in l), '')
    if 'python' in cmd.lower() or 'anaconda' in cmd.lower():
        print(name)
        print(cmd)
        print(sch)
        print()
