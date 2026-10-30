@echo off
REM KUJIRA Support System - production mode launcher with auto-restart watchdog loop.
REM Runs "next start" (built via "next build") instead of "next dev" to avoid
REM the dev-mode hot-reload hang issue. If the server process exits for any
REM reason, this loop restarts it automatically after a short delay.

cd /d "%~dp0"
set NODE_ENV=production

:LOOP
echo [%date% %time%] Starting KUJIRA Support (production mode)...
node_modules\.bin\next.cmd start -p 3001
echo [%date% %time%] Server exited. Restarting in 3 seconds...
timeout /t 3 /nobreak >nul
goto LOOP
