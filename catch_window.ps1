# 新規プロセスの出現を30秒間監視してログに記録する
$log = "C:\GensparkClaw\kujira-support\new_processes.log"
Add-Content $log "=== 監視開始 $(Get-Date) ==="

$known = @{}
Get-Process | ForEach-Object { $known[$_.Id] = $_.Name }

$end = (Get-Date).AddSeconds(120)
while ((Get-Date) -lt $end) {
    Get-Process | ForEach-Object {
        if (-not $known.ContainsKey($_.Id)) {
            $known[$_.Id] = $_.Name
            $line = "$(Get-Date -Format 'HH:mm:ss') 新プロセス: $($_.Name) (PID=$($_.Id)) MainWindowTitle='$($_.MainWindowTitle)' Path='$(try{$_.Path}catch{'N/A'})'"
            Add-Content $log $line
            Write-Host $line
        }
    }
    Start-Sleep -Milliseconds 500
}
Add-Content $log "=== 監視終了 $(Get-Date) ==="
