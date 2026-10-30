# verify-assets.ps1 - check that CSS/JS referenced by served HTML actually return 200
# Usage:  powershell -ExecutionPolicy Bypass -File .\verify-assets.ps1
# Exits 1 if any asset is 400/404 -> detects stale build (hash mismatch) immediately.
# ASCII only on purpose: Windows PowerShell 5.1 misreads UTF-8 .ps1 without BOM.
# [STALE_BUILD_CSS_V1]

$PORT = 3001
$PAGES = @('/dashboard', '/delivery')
$fail = 0
$checked = 0

foreach ($page in $PAGES) {
    try {
        $html = (Invoke-WebRequest "http://localhost:$PORT$page" -UseBasicParsing -TimeoutSec 15).Content
    } catch {
        Write-Host "[FAIL] cannot fetch $page : $_" -ForegroundColor Red
        $fail++
        continue
    }

    $assets = [regex]::Matches($html, '/_next/static/(?:css|chunks)/[^"''\\\s>]+?\.(?:css|js)') |
        ForEach-Object { $_.Value } | Select-Object -Unique

    $cssCount = 0
    foreach ($a in $assets) {
        $checked++
        if ($a -like '*.css') { $cssCount++ }
        try {
            $res = Invoke-WebRequest "http://localhost:$PORT$a" -UseBasicParsing -TimeoutSec 15
            if ($res.StatusCode -ne 200) {
                Write-Host "[FAIL] $page -> $a status=$($res.StatusCode)" -ForegroundColor Red
                $fail++
            }
        } catch {
            $code = $_.Exception.Response.StatusCode.value__
            Write-Host "[FAIL] $page -> $a status=$code (stale build: rebuild and restart)" -ForegroundColor Red
            $fail++
        }
    }

    # zero CSS means the unstyled-page bug
    if ($cssCount -eq 0) {
        Write-Host "[FAIL] $page has NO css reference (style broken)" -ForegroundColor Red
        $fail++
    }

    Write-Host "  $page : assets=$($assets.Count) css=$cssCount"
}

if ($fail -gt 0) {
    Write-Host ""
    Write-Host "[RESULT] FAIL - $fail broken asset(s) of $checked checked" -ForegroundColor Red
    exit 1
}
Write-Host ""
Write-Host "[RESULT] PASS - all $checked assets returned 200" -ForegroundColor Green
exit 0
