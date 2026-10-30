@echo off
REM Stops all KUJIRA Support System processes:
REM - the watchdog.ps1 health-check loop
REM - the start_production.bat restart loop (the cmd.exe window running it)
REM - the "next start" server process listening on port 3001
REM Note: since the server itself triggers this script via its own API,
REM this script waits a moment before killing the server process so the
REM HTTP response can be sent back to the browser first.

timeout /t 2 /nobreak >nul

REM Kill watchdog.ps1 (PowerShell processes running that script)
wmic process where "CommandLine like '%%watchdog.ps1%%'" call terminate >nul 2>&1

REM Kill the start_production.bat restart-loop cmd windows
wmic process where "Name='cmd.exe' and CommandLine like '%%start_production.bat%%'" call terminate >nul 2>&1

REM Kill whatever is listening on port 3001 (the next start server itself)
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":3001" ^| findstr LISTENING') do (
  taskkill /F /PID %%p >nul 2>&1
)

echo [%date% %time%] All KUJIRA Support processes stopped. > "%~dp0shutdown_log.txt"
