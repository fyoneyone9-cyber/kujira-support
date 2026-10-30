@echo off
chcp 65001 >nul
cd /d C:\GensparkClaw\kujira-support

set NODE_ENV=

powershell -NoProfile -Command "try { Invoke-WebRequest http://localhost:3001 -TimeoutSec 2 -UseBasicParsing -EA Stop | Out-Null; exit 1 } catch { exit 0 }"
if %errorlevel% == 1 (
  echo Already running. Opening browser...
  start chrome "http://localhost:3001"
  exit /b
)

echo Starting kujira-support dev server on port 3001...
:restart
node node_modules\next\dist\bin\next dev -p 3001
echo Dev server stopped. Restarting in 2 seconds...
timeout /t 2 /nobreak >nul
goto restart
