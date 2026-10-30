@echo off
rem =====================================================================
rem  kujira-support restart   [RESTART_V1 2026-10-29]
rem
rem  WHY THIS SCRIPT EXISTS:
rem    The `node` command on this machine resolves to a Genspark Claw shim:
rem      C:\Users\fyone\AppData\Roaming\Genspark Claw\bin\node.exe
rem    Running `next start` through it launches Genspark Claw.exe (Electron)
rem    which keeps serving a STALE .next build.
rem    Result: fixes never show up, the HTML asks for a JS chunk that no
rem    longer exists -> HTTP 400 -> "Application error: a client-side
rem    exception has occurred".
rem    ALWAYS use the real node.exe with a full path.
rem
rem  Usage:
rem    restart.bat         ... build + restart
rem    restart.bat clean   ... delete .next first, then build + restart
rem =====================================================================
setlocal
set ROOT=C:\GensparkClaw\kujira-support
set NODE=C:\Program Files\nodejs\node.exe
set PORT=3001
set PS=C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe

if not exist "%NODE%" (
  echo [NG] real node.exe not found: %NODE%
  pause
  exit /b 1
)
cd /d "%ROOT%"

echo === 1. stop process on port %PORT% ===
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":%PORT%" ^| findstr LISTENING') do (
  echo   kill PID=%%p
  taskkill /PID %%p /F >nul 2>&1
)
rem timeout is unusable in non-interactive shells; use ping as sleep
ping -n 4 127.0.0.1 >nul

if /i "%~1"=="clean" (
  echo === 1b. remove .next ===
  rmdir /s /q "%ROOT%\.next" 2>nul
)

echo === 2. typecheck ===
"%NODE%" node_modules\typescript\bin\tsc --noEmit -p tsconfig.json
if errorlevel 1 (
  echo [NG] tsc failed
  pause
  exit /b 1
)
echo   tsc OK

echo === 3. build ===
"%NODE%" node_modules\next\dist\bin\next build
if errorlevel 1 (
  echo [NG] build failed
  pause
  exit /b 1
)
echo   build OK

echo === 4. start (real node) ===
rem `start` fails under non-interactive shells, use Start-Process instead
"%PS%" -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%NODE%' -ArgumentList 'node_modules\next\dist\bin\next','start','-p','%PORT%' -WorkingDirectory '%ROOT%' -WindowStyle Minimized"
ping -n 21 127.0.0.1 >nul

echo === 5. verify ===
netstat -ano | findstr ":%PORT%" | findstr LISTENING
echo.
echo Open http://localhost:%PORT%/delivery and press Ctrl+F5
echo.
endlocal
