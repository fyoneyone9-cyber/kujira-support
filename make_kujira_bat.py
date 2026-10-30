content = b"""@echo off
title KUJIRA Support System
cd /d C:\\GensparkClaw\\kujira-support

echo [1/3] Stopping old process...
for /f "tokens=5" %%a in ('netstat -ano 2^>nul ^| findstr ":3001 "') do (
    taskkill /PID %%a /F >nul 2>&1
)
ping -n 3 127.0.0.1 >nul

echo [2/3] Starting server...
start "" /B cmd /c "node_modules\\.bin\\next.cmd start -p 3001 >> kujira_server.log 2>&1"

echo [3/3] Waiting for server...
:wait
ping -n 4 127.0.0.1 >nul
curl -s -f http://localhost:3001/ >nul 2>&1
if %errorlevel%==0 goto :open
echo    Still starting...
goto :wait

:open
echo OK! Opening browser...
start "" "http://localhost:3001/delivery"
ping -n 3 127.0.0.1 >nul
exit
"""

with open(r'C:\Users\fyone\Desktop\KUJIRA_Start.bat', 'wb') as f:
    f.write(content)
print('Done')
