import subprocess, sys
result = subprocess.run(
    [r'C:\Users\fyone\AppData\Roaming\Genspark Claw\bundled-resources\openclaw\node_modules\.bin\gsk.cmd',
     'upload', r'C:\GensparkClaw\kujira-support\docs\kiosk_preparation_guide_v4.pdf'],
    capture_output=True, text=True, encoding='utf-8'
)
print(result.stdout)
print(result.stderr)
