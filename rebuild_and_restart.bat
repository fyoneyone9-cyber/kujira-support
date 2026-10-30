@echo off
REM Rebuilds the production bundle and restarts the server.
REM Handles the case where start_production.bat watchdog loop is NOT running.

cd /d "%~dp0"
set LOGFILE=%~dp0rebuild_log.txt

echo [%date% %time%] Rebuild started > "%LOGFILE%"
call node_modules\.bin\next.cmd build >> "%LOGFILE%" 2>&1
set BUILD_RESULT=%ERRORLEVEL%
echo [%date% %time%] Build finished with exit code %BUILD_RESULT% >> "%LOGFILE%"

if %BUILD_RESULT% NEQ 0 (
  echo [%date% %time%] Build FAILED - server keeps running on old build. >> "%LOGFILE%"
  exit /b 1
)

echo [%date% %time%] Build succeeded. Killing port 3001... >> "%LOGFILE%"
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":3001" ^| findstr LISTENING') do (
  taskkill /F /PID %%p >> "%LOGFILE%" 2>&1
)

timeout /t 3 /nobreak >nul

REM ポート3001がまだ誰も使っていなければ自前でサーバーを起動
netstat -ano | findstr ":3001" | findstr LISTENING >nul 2>&1
if errorlevel 1 (
  echo [%date% %time%] Port 3001 free - launching start_server_loop.bat >> "%LOGFILE%"
  start "" /MIN cmd /c "%~dp0start_server_loop.bat"
) else (
  echo [%date% %time%] Port 3001 already up (watchdog restarted it). >> "%LOGFILE%"
)

echo [%date% %time%] Done. >> "%LOGFILE%"
