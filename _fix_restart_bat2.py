# -*- coding: utf-8 -*-
# powershell もPATHに無いのでフルパス指定にする。
import io, os

PS = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
print("powershell exists:", os.path.exists(PS))

p = r"C:\GensparkClaw\kujira-support\restart.bat"
s = io.open(p, encoding="utf-8").read()
s = s.replace("powershell -NoProfile", '"%PS%" -NoProfile', 1)
# 変数定義を追加
old = "set PORT=3001"
assert s.count(old) == 1
s = s.replace(old, old + "\nset PS=" + PS, 1)
io.open(p, "w", encoding="utf-8").write(s)
print("fixed")
