$anon = "sb_publishable_BBN8pHofRc1V3NWKoi81xg_hXZkH3dp"
$url  = "https://fjkpdejyusnttbhdmyxt.supabase.co/rest/v1/delivery_items?select=created_at&order=created_at.desc&limit=1"

try {
    $resp = Invoke-RestMethod -Uri $url -Headers @{
        "apikey"        = $anon
        "Authorization" = "Bearer $anon"
    } -Method Get -ErrorAction Stop
} catch {
    exit 0
}

if (-not $resp -or $resp.Count -eq 0) { exit 0 }

$lastImport = [datetime]::Parse($resp[0].created_at).ToLocalTime()
$hours = [math]::Floor(((Get-Date) - $lastImport).TotalHours)

if ($hours -ge 24) {
    $title = "KUJIRA Import Alert"
    $msg   = "No CSV import for ${hours}h. Please import now."
    Add-Type -AssemblyName System.Windows.Forms
    $notify = New-Object System.Windows.Forms.NotifyIcon
    $notify.Icon = [System.Drawing.SystemIcons]::Warning
    $notify.Visible = $true
    $notify.ShowBalloonTip(10000, $title, $msg, [System.Windows.Forms.ToolTipIcon]::Warning)
    Start-Sleep -Seconds 12
    $notify.Dispose()
}
