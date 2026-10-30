@echo off
setlocal EnableDelayedExpansion
REM =====================================================================
REM  KUJIRA Support - single instance launcher  [SINGLETON_V1 2026-10-29]
REM ---------------------------------------------------------------------
REM  There were 7 launcher scripts and the server was started 2-3 times,
REM  fighting over port 3001. Use ONLY this file from now on.
REM
REM  Usage:  kujira.bat          start (reuse if already running)
REM          kujira.bat restart  force restart
REM          kujira.bat stop     stop
REM =====================================================================
cd /d "%~dp0"
set PORT=3001
set URL=http://localhost:%PORT%/dashboard
set NODE=C:\Program Files\nodejs\node.exe

if /i "%~1"=="stop"    goto STOP
if /i "%~1"=="restart" goto RESTART
goto START

:STOP
echo [kujira] stopping...
call :KILL
echo [kujira] stopped.
exit /b 0

:RESTART
echo [kujira] restarting...
call :KILL
%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Start-Sleep -Seconds 3"
goto BOOT

:START
call :PING
if "!PINGOK!"=="1" (
  echo [kujira] already running - opening browser.
  call :OPEN
  exit /b 0
)
REM not responding but a stale process may hold the port
call :KILL

:BOOT
echo [kujira] starting... ^(takes about 20 seconds^)
start "KujiraSupport" /min "%NODE%" node_modules\next\dist\bin\next start -p %PORT%

for /l %%i in (1,1,30) do (
  %SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Start-Sleep -Seconds 2"
  call :PING
  if "!PINGOK!"=="1" goto READY
)
echo [kujira] failed to confirm startup. check the log.
exit /b 1

:READY
echo [kujira] started.
call :OPEN
exit /b 0

REM --------------------------------------------------------------
:PING
set PINGOK=0
%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "try{ Invoke-WebRequest 'http://localhost:%PORT%' -TimeoutSec 3 -UseBasicParsing -EA Stop | Out-Null; exit 0 }catch{ exit 1 }"
if %errorlevel%==0 set PINGOK=1
exit /b 0

REM --------------------------------------------------------------
:KILL
REM kill only next start/dev processes - leave other node apps alone
%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='node.exe'\" | Where-Object { $_.CommandLine -like '*next*start*' -or $_.CommandLine -like '*next*dev*' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -EA SilentlyContinue }"
REM also free the port if something still holds it
%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "Get-NetTCPConnection -LocalPort %PORT% -State Listen -EA SilentlyContinue | ForEach-Object { Stop-Process -Id $_.OwningProcess -Force -EA SilentlyContinue }"
exit /b 0

REM --------------------------------------------------------------
:OPEN
REM focus an existing dashboard window instead of opening a new tab
%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -Command "$w = Get-Process chrome,msedge -EA SilentlyContinue | Where-Object { $_.MainWindowTitle -match 'KUJIRA|dashboard' } | Select-Object -First 1; if($w){ $sig='[DllImport(\"user32.dll\")] public static extern bool SetForegroundWindow(IntPtr h);'; $t=Add-Type -MemberDefinition $sig -Name Fg -PassThru; $t::SetForegroundWindow($w.MainWindowHandle) | Out-Null } else { Start-Process '%URL%' }"
exit /b 0


