# -*- coding: utf-8 -*-
# `start` コマンドは非対話シェルで "Input redirection is not supported" になる。
# PowerShell の Start-Process を使う形に差し替える。
import io

p = r"C:\GensparkClaw\kujira-support\restart.bat"
s = io.open(p, encoding="utf-8").read()
old = 'start "kujira-support" /min "%NODE%" node_modules\\next\\dist\\bin\\next start -p %PORT%'
assert s.count(old) == 1, "anchor"
new = ('rem `start` fails under non-interactive shells, use Start-Process instead\n'
       'powershell -NoProfile -ExecutionPolicy Bypass -Command '
       '"Start-Process -FilePath \'%NODE%\' '
       '-ArgumentList \'node_modules\\next\\dist\\bin\\next\',\'start\',\'-p\',\'%PORT%\' '
       '-WorkingDirectory \'%ROOT%\' -WindowStyle Minimized"')
io.open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
print("fixed")
