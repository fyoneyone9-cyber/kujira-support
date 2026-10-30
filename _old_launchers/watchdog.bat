@echo off
chcp 65001 >nul
set LOGFILE=C:\GensparkClaw\kujira-support\watchdog.log

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "try { Invoke-WebRequest http://localhost:3001 -TimeoutSec 3 -UseBasicParsing -EA Stop | Out-Null; exit 0 } catch { exit 1 }"

if %errorlevel% == 0 exit /b 0

echo [%date% %time%] DOWN detected. Restarting... >> %LOGFILE%
start "" /B "C:\GensparkClaw\kujira-support\start_dev.bat"

timeout /t 30 /nobreak >nul

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "try { Invoke-WebRequest http://localhost:3001 -TimeoutSec 5 -UseBasicParsing -EA Stop | Out-Null; exit 0 } catch { exit 1 }"

if %errorlevel% == 0 (
  echo [%date% %time%] Recovered OK. >> %LOGFILE%
) else (
  echo [%date% %time%] Restart failed - still DOWN. >> %LOGFILE%
)
