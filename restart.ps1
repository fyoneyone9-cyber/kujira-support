# =====================================================================
#  kujira-support 再起動スクリプト  [RESTART_V1 2026-10-29]
# =====================================================================
#  🔴 必ずこれを使うこと。理由:
#   1. `node` コマンドの実体は Genspark Claw のシム
#        C:\Users\fyone\AppData\Roaming\Genspark Claw\bin\node.exe
#      これ経由で next start すると Genspark Claw.exe(Electron) が起動し、
#      **古い .next を掴んだまま**配信され続ける。
#      → 修正してビルドしても画面に反映されない / 存在しないJSを要求して
#        400 Bad Request → "Application error: a client-side exception" になる。
#   2. ビルド後は必ず旧プロセスを止めてから起動する(ハッシュ不一致防止)。
#
#  使い方:
#     powershell -ExecutionPolicy Bypass -File restart.ps1          # ビルド+再起動
#     powershell -ExecutionPolicy Bypass -File restart.ps1 -Clean   # .next削除から
# =====================================================================
param([switch]$Clean, [switch]$NoBuild)

$ErrorActionPreference = 'Continue'
$ROOT = "C:\GensparkClaw\kujira-support"
$NODE = "C:\Program Files\nodejs\node.exe"      # ← 本物のNode。絶対にフルパス指定
$PORT = 3001

if (-not (Test-Path $NODE)) { Write-Host "[NG] 本物のnode.exeが見つかりません: $NODE" -ForegroundColor Red; exit 1 }
Set-Location $ROOT

Write-Host "=== 1. 既存プロセス停止 ===" -ForegroundColor Cyan
$owners = Get-NetTCPConnection -LocalPort $PORT -EA SilentlyContinue | Select-Object -Expand OwningProcess -Unique
foreach ($o in $owners) {
  $p = Get-CimInstance Win32_Process -Filter "ProcessId=$o" -EA SilentlyContinue
  if ($p) { Write-Host ("  kill PID={0} {1}" -f $o, $p.Name) }
  Stop-Process -Id $o -Force -EA SilentlyContinue
}
Start-Sleep 3

if ($Clean) {
  Write-Host "=== 1b. .next 削除 ===" -ForegroundColor Cyan
  Remove-Item "$ROOT\.next" -Recurse -Force -EA SilentlyContinue
}

if (-not $NoBuild) {
  Write-Host "=== 2. 型チェック ===" -ForegroundColor Cyan
  $t = Start-Process -FilePath $NODE -ArgumentList 'node_modules\typescript\bin\tsc','--noEmit','-p','tsconfig.json' `
       -NoNewWindow -Wait -PassThru -RedirectStandardOutput "$ROOT\_tsc.out" -RedirectStandardError "$ROOT\_tsc.err"
  if ($t.ExitCode -ne 0) {
    Write-Host "[NG] tsc 失敗" -ForegroundColor Red
    Get-Content "$ROOT\_tsc.out" -EA SilentlyContinue | Select-Object -First 15
    exit 1
  }
  Write-Host "  tsc OK" -ForegroundColor Green

  Write-Host "=== 3. ビルド ===" -ForegroundColor Cyan
  $b = Start-Process -FilePath $NODE -ArgumentList 'node_modules\next\dist\bin\next','build' `
       -NoNewWindow -Wait -PassThru -RedirectStandardOutput "$ROOT\_build.out" -RedirectStandardError "$ROOT\_build.err"
  if ($b.ExitCode -ne 0) {
    Write-Host "[NG] build 失敗" -ForegroundColor Red
    Get-Content "$ROOT\_build.err" -EA SilentlyContinue | Select-Object -Last 15
    exit 1
  }
  Write-Host "  build OK" -ForegroundColor Green
}

Write-Host "=== 4. 起動(本物のnode) ===" -ForegroundColor Cyan
Start-Process -FilePath $NODE -ArgumentList 'node_modules\next\dist\bin\next','start','-p',"$PORT" `
  -WorkingDirectory $ROOT -WindowStyle Minimized
Start-Sleep 20

Write-Host "=== 5. 検証 ===" -ForegroundColor Cyan
$owner = Get-NetTCPConnection -LocalPort $PORT -State Listen -EA SilentlyContinue | Select-Object -First 1 -Expand OwningProcess
if ($owner) {
  $pp = Get-CimInstance Win32_Process -Filter "ProcessId=$owner" -EA SilentlyContinue
  Write-Host ("  listener: PID={0} {1}" -f $owner, $pp.Name)
  if ($pp.Name -ne 'node.exe') {
    Write-Host "  [警告] node.exe 以外が掴んでいます。古いビルドを配信する恐れあり" -ForegroundColor Yellow
  }
}
try {
  $r = Invoke-WebRequest "http://localhost:$PORT/delivery" -TimeoutSec 20 -UseBasicParsing
  Write-Host ("  /delivery = {0}" -f $r.StatusCode) -ForegroundColor Green
  # HTMLが要求するJSが実在するか照合（400の再発防止）
  $js = [regex]::Matches($r.Content, '/_next/static/chunks/[^"]+\.js') | ForEach-Object { $_.Value } | Select-Object -Unique
  $miss = 0
  foreach ($u in $js) {
    $f = Join-Path $ROOT (".next\static" + ($u -replace '^/_next/static','' -replace '/','\'))
    if (-not (Test-Path -LiteralPath $f)) { Write-Host "  [NG] 参照されているが存在しない: $u" -ForegroundColor Red; $miss++ }
  }
  if ($miss -eq 0) { Write-Host ("  JS照合 OK ({0}本すべて実在)" -f $js.Count) -ForegroundColor Green }
} catch {
  Write-Host "  [NG] /delivery に接続できません: $_" -ForegroundColor Red
}
Write-Host "=== 完了 ===" -ForegroundColor Cyan
