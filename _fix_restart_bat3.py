# -*- coding: utf-8 -*-
# "Input redirection is not supported" は timeout コマンドが原因。
# 非対話シェルでは使えないので ping で代用する。
import io

p = r"C:\GensparkClaw\kujira-support\restart.bat"
s = io.open(p, encoding="utf-8").read()
s = s.replace("timeout /t 3 /nobreak >nul",
              "rem timeout is unusable in non-interactive shells; use ping as sleep\n"
              "ping -n 4 127.0.0.1 >nul")
s = s.replace("timeout /t 20 /nobreak >nul", "ping -n 21 127.0.0.1 >nul")
io.open(p, "w", encoding="utf-8").write(s)
print("fixed")
