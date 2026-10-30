$url     = "http://localhost:3001"
$bat     = "C:\GensparkClaw\kujira-support\start_production.bat"
$logFile = "C:\GensparkClaw\kujira-support\watchdog.log"

function Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content $logFile "[$ts] $msg"
}

# ログが10KB超えたら古い行を削除して圧縮
if ((Test-Path $logFile) -and (Get-Item $logFile).Length -gt 10240) {
    $lines = Get-Content $logFile
    Set-Content $logFile ($lines | Select-Object -Last 100)
}

try {
    $res = Invoke-WebRequest $url -TimeoutSec 5 -UseBasicParsing -EA Stop
    # 正常（2xx/3xx） - 何もしない
} catch {
    Log "DOWN detected. Starting production server..."
    # start_production.bat をバックグラウンドで起動
    $si = New-Object System.Diagnostics.ProcessStartInfo
    $si.FileName        = "cmd.exe"
    $si.Arguments       = "/c `"$bat`""
    $si.WorkingDirectory = "C:\GensparkClaw\kujira-support"
    $si.WindowStyle     = [System.Diagnostics.ProcessWindowStyle]::Hidden
    $si.CreateNoWindow  = $true
    [System.Diagnostics.Process]::Start($si) | Out-Null

    # 30秒待って死活確認
    Start-Sleep -Seconds 30
    try {
        Invoke-WebRequest $url -TimeoutSec 5 -UseBasicParsing -EA Stop | Out-Null
        Log "Recovered OK."
    } catch {
        Log "Restart FAILED - still DOWN after 30s."
    }
}
