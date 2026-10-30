import subprocess, sys
sys.stdout.reconfigure(encoding='utf-8')
result = subprocess.run(
    [r'C:\Users\fyone\AppData\Roaming\Genspark Claw\bundled-resources\openclaw\node_modules\.bin\gsk.cmd',
     'summarize', r'C:\GensparkClaw\kujira-support\docs\kiosk_preparation_guide_v4.pdf',
     '--question', 'このPDFの全内容を詳しく抽出してください。お客様がシステム導入前に準備すべきこと、確認事項、必要書類・情報、手順、注意事項をすべて章・項目別に列挙してください。'],
    capture_output=True, text=True, encoding='utf-8', errors='replace'
)
print(result.stdout[-5000:] if len(result.stdout) > 5000 else result.stdout)
print(result.stderr[-2000:] if len(result.stderr) > 2000 else result.stderr)
