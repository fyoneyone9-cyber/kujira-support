@echo off
REM KUJIRA Support System - startup launcher.
REM Launches the production server (with its own auto-restart loop) and the
REM health-check watchdog, both minimized, in the background.
REM This file is meant to be placed as a shortcut in the Windows Startup folder
REM so both processes come back automatically after reboot/logon.

start "KujiraSupportServer" /min cmd /c "C:\GensparkClaw\kujira-support\start_production.bat"
timeout /t 5 /nobreak >nul
start "KujiraSupportWatchdog" /min C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe -NoProfile -ExecutionPolicy Bypass -File "C:\GensparkClaw\kujira-support\watchdog.ps1"
