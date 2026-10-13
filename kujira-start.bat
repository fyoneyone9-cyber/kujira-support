@echo off
pushd C:\GensparkClaw\kujira-support
echo kujira-support ‹N“®’† (port 3001)...
start cmd /k node_modules\.bin\next.cmd dev -p 3001
timeout /t 5 /nobreak
start http://localhost:3001/dashboard
popd
