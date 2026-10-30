# work_alert.ps1 - 作業開始時刻アラーム (1時間前・30分前)
$SUPABASE_URL = "https://fjkpdejyusnttbhdmyxt.supabase.co"
$SUPABASE_KEY = "sb_publishable_BBN8pHofRc1V3NWKoi81xg_hXZkH3dp"

function Show-Toast($title, $message) {
    $xml = @"
<toast>
  <visual>
    <binding template="ToastGenericImageAndText04">
      <text id="1">$title</text>
      <text id="2">$message</text>
    </binding>
  </visual>
  <audio src="ms-winsoundevent:Notification.Reminder"/>
</toast>
"@
    [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
    [Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime] | Out-Null
    $xdoc = New-Object Windows.Data.Xml.Dom.XmlDocument
    $xdoc.LoadXml($xml)
    $toast = New-Object Windows.UI.Notifications.ToastNotification $xdoc
    $notifier = [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("くじらサポート")
    $notifier.Show($toast)
}

$now = Get-Date
$today = $now.ToString("yyyy-MM-dd")

# Supabaseから今日の作業予定を取得
$headers = @{
    "apikey"        = $SUPABASE_KEY
    "Authorization" = "Bearer $SUPABASE_KEY"
}

try {
    $url = "$SUPABASE_URL/rest/v1/delivery_items?select=id,client_name,install_address,worker_name,work_date,work_start_time&work_date=eq.$today&work_start_time=not.is.null"
    $items = Invoke-RestMethod -Uri $url -Headers $headers -Method Get -TimeoutSec 10
} catch {
    exit 0
}

$alerted = @()
$alertFile = "$env:TEMP\work_alert_sent.txt"
if (Test-Path $alertFile) {
    $alerted = Get-Content $alertFile
}

foreach ($item in $items) {
    if (-not $item.work_start_time) { continue }

    $startStr = "$today $($item.work_start_time.Substring(0,5))"
    try { $startTime = [DateTime]::Parse($startStr) } catch { continue }

    $diffMin = ($startTime - $now).TotalMinutes

    $label60 = "$($item.id)_60"
    $label30 = "$($item.id)_30"

    $name = $item.client_name
    $addr = $item.install_address
    $worker = $item.worker_name
    $timeStr = $item.work_start_time.Substring(0,5)

    if ($diffMin -gt 55 -and $diffMin -le 65 -and $alerted -notcontains $label60) {
        Show-Toast "🔔 作業開始 1時間前" "$name`n$addr`n作業員: $worker`n開始: $timeStr"
        Add-Content $alertFile $label60
    }
    if ($diffMin -gt 25 -and $diffMin -le 35 -and $alerted -notcontains $label30) {
        Show-Toast "⚠️ 作業開始 30分前" "$name`n$addr`n作業員: $worker`n開始: $timeStr"
        Add-Content $alertFile $label30
    }
}

# 翌日0時以降に古いアラート履歴を削除
if ($now.Hour -eq 0 -and $now.Minute -lt 5) {
    Remove-Item $alertFile -Force -ErrorAction SilentlyContinue
}
