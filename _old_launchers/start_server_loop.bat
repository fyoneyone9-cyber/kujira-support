@echo off
cd /d "%~dp0"
set NODE_ENV=production
:LOOP
echo [%date% %time%] Starting KUJIRA Support...
node_modules\.bin\next.cmd start -p 3001
echo [%date% %time%] Server exited. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto LOOP
