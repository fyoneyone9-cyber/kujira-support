# deploy.ps1 - ALWAYS do build -> restart -> verify as one atomic operation.
# Usage:  powershell -ExecutionPolicy Bypass -File .\deploy.ps1
# Why: running "next build" while "next start" is live leaves the server serving
#      old HTML that points at CSS hashes no longer on disk -> 400 -> unstyled page.
# ASCII only on purpose: Windows PowerShell 5.1 misreads UTF-8 .ps1 without BOM.
# [STALE_BUILD_CSS_V1]

$ErrorActionPreference = 'Stop'
$ROOT = 'C:\GensparkClaw\kujira-support'
$PORT = 3001
Set-Location $ROOT

function Stop-NextServer {
    $procs = @(Get-CimInstance Win32_Process -Filter "Name='node.exe'" |
        Where-Object { $_.CommandLine -like '*next*' -and $_.CommandLine -like "*$PORT*" })
    foreach ($p in $procs) {
        Write-Host "[stop] PID $($p.ProcessId)"
        Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    }
    if ($procs.Count -gt 0) { Start-Sleep -Seconds 2 }
}

Write-Host '=== 1/4 stop ==='
Stop-NextServer

Write-Host '=== 2/4 build ==='
$build = Start-Process -FilePath 'node' `
    -ArgumentList 'node_modules\next\dist\bin\next', 'build' `
    -WorkingDirectory $ROOT -NoNewWindow -Wait -PassThru
if ($build.ExitCode -ne 0) {
    Write-Host "[FAIL] build exit=$($build.ExitCode) - server NOT started" -ForegroundColor Red
    exit 1
}

Write-Host '=== 3/4 start ==='
Start-Process -FilePath 'node' `
    -ArgumentList 'node_modules\next\dist\bin\next', 'start', '-p', "$PORT" `
    -WorkingDirectory $ROOT -WindowStyle Hidden

$up = $false
for ($i = 0; $i -lt 40; $i++) {
    Start-Sleep -Seconds 1
    try {
        $r = Invoke-WebRequest "http://localhost:$PORT/dashboard" -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -eq 200) { $up = $true; break }
    } catch { }
}
if (-not $up) {
    Write-Host '[FAIL] server did not come up' -ForegroundColor Red
    exit 1
}

Write-Host '=== 4/4 verify ==='
$psExe = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
& $psExe -ExecutionPolicy Bypass -File (Join-Path $ROOT 'verify-assets.ps1')
$code = $LASTEXITCODE
if ($code -eq 0) { Write-Host '[DONE] deploy OK' -ForegroundColor Green }
exit $code
