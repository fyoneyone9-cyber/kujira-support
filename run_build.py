import subprocess, sys
r = subprocess.run(
    ['C:\\Users\\fyone\\anaconda3\\python.exe', 'C:\\GensparkClaw\\kujira-support\\do_build.py'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
out = r.stdout + r.stderr
# エラー行だけ抽出
lines = out.splitlines()
errors = [l for l in lines if any(k in l for k in ['error', 'Error', 'failed', 'Type', 'Cannot', 'Expected', 'Unexpected', '×'])]
with open(r'C:\GensparkClaw\kujira-support\build_error.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(errors[-80:]))
print('\n'.join(errors[-40:]))
print('returncode:', r.returncode)
