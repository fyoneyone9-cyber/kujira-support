import subprocess, sys, os
sys.stdout.reconfigure(encoding='utf-8')
os.chdir(r'C:\GensparkClaw\kujira-support')
r = subprocess.run(
    [r'node_modules\.bin\next.cmd', 'build'],
    capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=120
)
print('=== STDOUT (last 3000) ===')
print(r.stdout[-3000:])
print('=== STDERR (last 2000) ===')
print(r.stderr[-2000:])
print('returncode:', r.returncode)
